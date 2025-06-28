# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FurnitureFinish(models.Model):
    _name = 'x_furniture_finish'
    _description = 'Furniture Finish Option'
    _order = 'x_finish_type_id, x_name'
    _sql_constraints = [
        ('unique_code', 'UNIQUE(x_code)', 'Finish code must be unique'),
        ('positive_cost', 'CHECK(x_cost_usd >= 0)', 'Cost must be non-negative')
    ]
    
    # Field definitions
    x_finish_type_id = fields.Many2one(
        'x_furniture_finish_type',
        string="Finish Type"
    )
    x_code = fields.Char(
        string="Finish Code",
        required=True,
        size=20
    )
    x_name = fields.Char(
        string="Finish Name",
        size=255
    )
    x_color = fields.Char(
        string="Color",
        size=100
    )
    x_cost_usd = fields.Float(
        string="Cost (USD)",
        digits=(8, 2),
        default=0.0
    )
    x_cost_unit = fields.Selection(
        [('unit', 'Unit'), ('m2', 'Square Meter'), ('linear_m', 'Linear Meter')],
        string="Cost Unit",
        default='unit'
    )
    x_supplier = fields.Char(
        string="Supplier",
        size=100
    )
    x_supplier_code = fields.Char(
        string="Supplier Code",
        size=50
    )
    x_lead_time_impact_days = fields.Integer(
        string="Lead Time Impact (Days)",
        default=0
    )
    x_active = fields.Boolean(
        string="Active",
        default=True
    )