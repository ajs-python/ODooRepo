# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # ========================================
    # FIELD DEFINITIONS WITH DEFAULTS
    # ========================================
    
    # Category and classification fields
    x_furniture_category = fields.Selection([
        ('seating', 'Seating'),
        ('table', 'Table'), 
        ('joinery', 'Joinery'),
        ('outdoor', 'Outdoor')
    ], string="Furniture Category")
    
    x_furniture_sub_type = fields.Char(
        string="Sub Type",
        size=100
    )
    
    x_furniture_brand = fields.Char(
        string="Brand",
        size=100
    )
    
    x_furniture_vendor_id = fields.Many2one(
        'res.partner',
        string="Vendor",
        domain="[('is_company', '=', True)]"
    )
    
    # Cost and pricing fields
    x_furniture_base_cost_usd = fields.Float(
        string="Base Cost (USD)",
        digits=(10, 2)
    )
    
    # Lead time and logistics
    x_furniture_lead_time_days = fields.Integer(
        string="Lead Time (Days)",
        default=0
    )
    
    x_furniture_package_volume_m3 = fields.Float(
        string="Package Volume (m³)",
        digits=(8, 3)
    )
    
    x_furniture_weight_kg = fields.Float(
        string="Weight (kg)",
        digits=(8, 2)
    )
    
    # Product characteristics
    x_furniture_warranty_years = fields.Integer(
        string="Warranty (Years)", 
        default=0
    )
    
    x_furniture_warranty_cost = fields.Float(
        string="Warranty Cost (USD)",
        default=0.0,
        digits=(8, 2),
        help="Warranty cost per unit in USD"
    )
    
    x_furniture_assembly_required = fields.Boolean(
        string="Assembly Required",
        default=False
    )
    
    x_furniture_commercial_grade = fields.Boolean(
        string="Commercial Grade",
        default=False
    )
    
    x_furniture_catalog_order = fields.Selection([
        ('contract', 'Contract'),
        ('showroom', 'Showroom'),
        ('catalogue', 'Catalogue')
    ], string="Catalog Order")
    
    # Relationship field
    x_furniture_finish_line_ids = fields.One2many(
        'x_furniture_product_finish_line',
        'x_product_tmpl_id',
        string="Compatible Finishes"
    )
    
    # ========================================
    # COMPUTED FIELDS
    # ========================================
    
    x_furniture_china_cost_usd = fields.Float(
        string="China Cost (USD)",
        compute='_compute_furniture_china_cost_usd',
        store=True,
        digits=(10, 2),
        help="Base cost + minimum finish cost"
    )
    
    x_furniture_freight_budget = fields.Float(
        string="Freight Budget",
        compute='_compute_furniture_freight_budget',
        store=True,
        digits=(10, 2),
        help="Package volume × freight rate"
    )
    
    x_furniture_landed_cost = fields.Float(
        string="Landed Cost",
        compute='_compute_furniture_landed_cost',
        store=True,
        digits=(10, 2),
        help="China cost + freight"
    )
    
    x_furniture_total_cogs_usd = fields.Float(
        string="Total COGS (USD)",
        compute='_compute_furniture_total_cogs_usd',
        store=True,
        digits=(10, 2),
        help="Landed cost + warranty cost"
    )
    
    x_furniture_total_cogs_aud = fields.Float(
        string="Total COGS (AUD)",
        compute='_compute_furniture_total_cogs_aud',
        store=True,
        digits=(10, 2),
        help="USD COGS converted to AUD"
    )
    
    x_furniture_wholesale_price = fields.Float(
        string="Wholesale Price",
        compute='_compute_furniture_wholesale_price',
        store=True,
        digits=(10, 2),
        help="AUD COGS / margin factor"
    )
    
    x_furniture_rrp = fields.Float(
        string="RRP",
        compute='_compute_furniture_rrp',
        store=True,
        digits=(10, 2),
        help="Wholesale price × RRP multiplier"
    )
    
    x_furniture_margin_amount = fields.Float(
        string="Margin Amount",
        compute='_compute_furniture_margin',
        store=True,
        digits=(10, 2),
        help="Wholesale - COGS"
    )
    
    x_furniture_margin_percent = fields.Float(
        string="Margin %",
        compute='_compute_furniture_margin',
        store=True,
        digits=(5, 2),
        help="Margin as percentage of wholesale price"
    )
    
    # ========================================
    # COMPUTED FIELD METHODS
    # ========================================
    
    @api.depends('x_furniture_base_cost_usd', 'x_furniture_finish_line_ids')
    def _compute_furniture_china_cost_usd(self):
        """Calculate China cost including base cost and minimum finish cost."""
        for record in self:
            base_cost = record.x_furniture_base_cost_usd or 0.0
            
            # Calculate minimum finish cost from finish lines
            finish_cost = 0.0
            if record.x_furniture_finish_line_ids:
                finish_costs = []
                for line in record.x_furniture_finish_line_ids:
                    if line.x_finish_id and line.x_finish_id.x_cost_usd:
                        cost = line.x_finish_id.x_cost_usd
                        
                        # Handle cost unit conversions
                        if line.x_finish_id.x_cost_unit == 'm2' and line.x_surface_area_m2:
                            cost = cost * line.x_surface_area_m2
                        elif line.x_finish_id.x_cost_unit == 'linear_m':
                            # Assume 1 linear meter if not specified
                            logger.warning(f"Linear meter cost for {line.x_finish_id.x_name} - using 1m")
                        
                        finish_costs.append(cost)
                
                # Use minimum finish cost if available
                if finish_costs:
                    finish_cost = min(finish_costs)
            
            record.x_furniture_china_cost_usd = base_cost + finish_cost
    
    @api.depends('x_furniture_package_volume_m3')
    def _compute_furniture_freight_budget(self):
        """Calculate freight budget based on package volume."""
        for record in self:
            freight_rate = float(self.env['ir.config_parameter'].sudo().get_param(
                'furniture.freight_rate_param', 160.93
            ))
            volume = record.x_furniture_package_volume_m3 or 0.0
            record.x_furniture_freight_budget = freight_rate * volume
    
    @api.depends('x_furniture_china_cost_usd', 'x_furniture_freight_budget')
    def _compute_furniture_landed_cost(self):
        """Calculate landed cost (China cost + freight)."""
        for record in self:
            record.x_furniture_landed_cost = (
                (record.x_furniture_china_cost_usd or 0.0) +
                (record.x_furniture_freight_budget or 0.0)
            )
    
    @api.depends('x_furniture_landed_cost', 'x_furniture_warranty_cost')
    def _compute_furniture_total_cogs_usd(self):
        """Calculate total COGS in USD including warranty cost."""
        for record in self:
            # Add warranty cost to landed cost
            record.x_furniture_total_cogs_usd = (
                (record.x_furniture_landed_cost or 0.0) +
                (record.x_furniture_warranty_cost or 0.0)
            )
    
    @api.depends('x_furniture_total_cogs_usd')
    def _compute_furniture_total_cogs_aud(self):
        """Convert total COGS to AUD."""
        for record in self:
            usd_aud_rate = float(self.env['ir.config_parameter'].sudo().get_param(
                'furniture.usd_aud_rate_param', 0.665
            ))
            if usd_aud_rate:
                record.x_furniture_total_cogs_aud = (
                    (record.x_furniture_total_cogs_usd or 0.0) / usd_aud_rate
                )
            else:
                record.x_furniture_total_cogs_aud = 0.0
    
    @api.depends('x_furniture_total_cogs_aud')
    def _compute_furniture_wholesale_price(self):
        """Calculate wholesale price based on target margin."""
        for record in self:
            margin_factor = float(self.env['ir.config_parameter'].sudo().get_param(
                'furniture.margin_factor_param', 0.7
            ))
            if margin_factor:
                record.x_furniture_wholesale_price = (
                    (record.x_furniture_total_cogs_aud or 0.0) / margin_factor
                )
            else:
                record.x_furniture_wholesale_price = 0.0
    
    @api.depends('x_furniture_wholesale_price')
    def _compute_furniture_rrp(self):
        """Calculate RRP based on wholesale price."""
        for record in self:
            rrp_multiplier = float(self.env['ir.config_parameter'].sudo().get_param(
                'furniture.rrp_multiplier_param', 1.8
            ))
            record.x_furniture_rrp = (
                (record.x_furniture_wholesale_price or 0.0) * rrp_multiplier
            )
    
    @api.depends('x_furniture_wholesale_price', 'x_furniture_total_cogs_aud')
    def _compute_furniture_margin(self):
        """Calculate margin amount and percentage."""
        for record in self:
            wholesale = record.x_furniture_wholesale_price or 0.0
            cogs = record.x_furniture_total_cogs_aud or 0.0
            
            record.x_furniture_margin_amount = wholesale - cogs
            
            if wholesale:
                record.x_furniture_margin_percent = (
                    record.x_furniture_margin_amount / wholesale * 100
                )
            else:
                record.x_furniture_margin_percent = 0.0
    
    # ========================================
    # CONSTRAINT METHODS
    # ========================================
    
    @api.constrains('x_furniture_base_cost_usd', 'x_furniture_package_volume_m3', 'x_furniture_weight_kg')
    def _check_furniture_positive_costs(self):
        """Ensure costs and dimensions are positive."""
        for record in self:
            if record.x_furniture_base_cost_usd and record.x_furniture_base_cost_usd < 0:
                raise ValidationError("Base cost must be positive")
            if record.x_furniture_package_volume_m3 and record.x_furniture_package_volume_m3 < 0:
                raise ValidationError("Package volume must be positive")
            if record.x_furniture_weight_kg and record.x_furniture_weight_kg < 0:
                raise ValidationError("Weight must be positive")
    
    @api.constrains('x_furniture_catalog_order', 'x_furniture_margin_percent')
    def _check_furniture_minimum_margin(self):
        """Ensure minimum margin requirements are met."""
        for record in self:
            if (record.x_furniture_catalog_order and 
                record.x_furniture_margin_percent and 
                record.x_furniture_margin_percent < 30):
                raise ValidationError(
                    f"Product {record.name} margin {record.x_furniture_margin_percent:.1f}% "
                    f"is below 30% minimum"
                )