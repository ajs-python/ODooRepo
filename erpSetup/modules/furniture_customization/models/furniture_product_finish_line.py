# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FurnitureProductFinishLine(models.Model):
    _name = 'x_furniture_product_finish_line'
    _description = 'Product Finish Compatibility'
    _order = 'x_product_tmpl_id, x_finish_position'
    _sql_constraints = [
        ('unique_product_finish_position', 
         'UNIQUE(x_product_tmpl_id, x_finish_id, x_finish_position)', 
         'Product-finish-position combination must be unique')
    ]
    
    # Field definitions
    x_product_tmpl_id = fields.Many2one(
        'product.template',
        string="Product Template"
    )
    x_finish_id = fields.Many2one(
        'x_furniture_finish',
        string="Finish"
    )
    x_finish_position = fields.Integer(
        string="Finish Position",
        help="1=Finish1, 2=Finish2, etc."
    )
    x_surface_area_m2 = fields.Float(
        string="Surface Area (m²)",
        digits=(8, 3),
        default=0.0
    )
    x_is_required = fields.Boolean(
        string="Required",
        default=False
    )
    x_is_default = fields.Boolean(
        string="Default",
        default=False
    )
    x_surcharge = fields.Float(
        string="Surcharge",
        digits=(8, 2),
        default=0.0
    )