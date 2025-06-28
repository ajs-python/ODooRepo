# -*- coding: utf-8 -*-
{
    'name': 'Furniture Customization',
    'version': '1.1.0',
    'category': 'Sales/Sales',
    'summary': 'Furniture product customizations with computed pricing fields and default values',
    'description': """
        Furniture Customization Module
        ==============================
        
        This module provides:
        
        1. Custom Models (Tables):
        - x_furniture_finish_type - Finish type categories
        - x_furniture_finish - Finish options with costs
        - x_furniture_product_finish_line - Product-finish relationships
        
        2. Default Values for Fields:
        - Lead time days (default: 0)
        - Warranty years (default: 0)
        - Warranty cost (default: 0.0)
        - Assembly required (default: False)
        - Commercial grade (default: False)
        - Finish type sequence (default: 10)
        - Active flags (default: True)
        - Cost units (default: 'unit')
        - Surface areas and surcharges (default: 0.0)
        
        2. Computed Fields:
        - Cost calculations (China cost, freight, landed cost)
        - Pricing calculations (COGS, wholesale, RRP)
        - Margin calculations
        - Warranty cost tracking
        
        3. Business Constraints:
        - Positive cost validation
        - Minimum 30% margin for catalog items
        
        Computed fields automatically calculate based on:
        - Base manufacturing costs
        - Finish selections and costs
        - Freight rates from system parameters
        - Exchange rates from system parameters
        - Margin targets from system parameters
    """,
    'author': 'Property Portal',
    'depends': ['base', 'product', 'sale'],
    'data': [
        'data/system_parameters.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}