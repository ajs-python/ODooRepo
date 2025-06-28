# Furniture Customization Module

This Odoo module provides computed field implementations and default values for the Klyde furniture schema.

## Purpose

Since Odoo's API has limitations:
1. Cannot create computed fields with Python code
2. Cannot set default values for fields via API
3. Cannot set field digits/precision via API

This module contains:
- Custom model definitions (x_furniture_finish_type, x_furniture_finish, x_furniture_product_finish_line)
- Python methods for all computed fields
- Default value definitions for all fields that require defaults
- Business constraint implementations
- Security access rules for the custom models

## Default Values

The module sets default values that cannot be set via API:

### Product Template Fields
- `x_furniture_lead_time_days` = 0
- `x_furniture_warranty_years` = 0  
- `x_furniture_warranty_cost` = 0.0
- `x_furniture_assembly_required` = False
- `x_furniture_commercial_grade` = False

### Finish Type Fields
- `x_sequence` = 10
- `x_active` = True

### Finish Fields
- `x_cost_usd` = 0.0
- `x_cost_unit` = 'unit'
- `x_lead_time_impact_days` = 0
- `x_active` = True

### Product Finish Line Fields
- `x_surface_area_m2` = 0.0
- `x_is_required` = False
- `x_is_default` = False
- `x_surcharge` = 0.0

## Computed Fields

The module implements the following computed pricing fields on `product.template`:

1. **x_furniture_china_cost_usd** - Base cost + minimum finish cost
2. **x_furniture_freight_budget** - Package volume × freight rate
3. **x_furniture_landed_cost** - China cost + freight
4. **x_furniture_total_cogs_usd** - Landed cost + warranty cost
5. **x_furniture_total_cogs_aud** - USD COGS converted to AUD
6. **x_furniture_wholesale_price** - AUD COGS / margin factor
7. **x_furniture_rrp** - Wholesale price × RRP multiplier
8. **x_furniture_margin_amount** - Wholesale - COGS
9. **x_furniture_margin_percent** - Margin as percentage

## System Parameters

The module uses the following system parameters:
- `furniture.freight_rate_param` - Freight rate per m³ (default: 160.93)
- `furniture.usd_aud_rate_param` - USD to AUD rate (default: 0.665)
- `furniture.margin_factor_param` - Target margin factor (default: 0.7)
- `furniture.rrp_multiplier_param` - RRP multiplier (default: 1.8)

## Constraints

- All costs and dimensions must be positive
- Products with catalog order must maintain 30% minimum margin

## Installation

1. Zip this module directory
2. Upload via Odoo Apps interface
3. Install the module
4. The computed fields will automatically recalculate when dependencies change

## Dependencies

- base
- product
- sale