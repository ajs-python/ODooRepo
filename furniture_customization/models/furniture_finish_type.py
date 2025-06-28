# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FurnitureFinishType(models.Model):
    _name = 'x_furniture_finish_type'
    _description = 'Furniture Finish Type'
    _order = 'x_sequence, x_name'
    _sql_constraints = [
        ('unique_code', 'UNIQUE(x_code)', 'Finish type code must be unique')
    ]
    
    # Field definitions
    x_name = fields.Char(
        string="Finish Type Name",
        size=100
    )
    x_code = fields.Char(
        string="Type Code",
        size=25
    )
    x_sequence = fields.Integer(
        string="Sequence",
        default=10
    )
    x_active = fields.Boolean(
        string="Active",
        default=True
    )