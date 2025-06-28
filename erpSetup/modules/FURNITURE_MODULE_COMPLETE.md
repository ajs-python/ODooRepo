# Furniture Customization Module - Complete Package

## Module Overview
**Version**: 1.1.0  
**Location**: `/Users/ajs/AIOrchestration/PropertyPortal/erpSetup/modules/furniture_customization.zip`

## What's Included

### 1. Custom Models (Tables)
- `x_furniture_finish_type` - Finish categories (Fabric, Powder Coat, etc.)
- `x_furniture_finish` - Specific finish options with costs
- `x_furniture_product_finish_line` - Links products to compatible finishes

### 2. Product Template Extensions
**Regular Fields:**
- Category, sub-type, brand
- Vendor relationship
- Base cost, lead time, volume, weight
- Warranty years and cost
- Assembly required, commercial grade flags
- Catalog order

**Computed Fields with Python Code:**
- China cost (base + finish)
- Freight budget
- Landed cost
- Total COGS in USD and AUD
- Wholesale price
- RRP
- Margin amount and percentage

### 3. System Parameters
- `furniture.freight_rate_param` = 160.93
- `furniture.usd_aud_rate_param` = 0.665
- `furniture.margin_factor_param` = 0.7
- `furniture.rrp_multiplier_param` = 1.8

### 4. Security Access Rules
- Read access for all users
- Full access for system managers

### 5. Default Values
All fields have proper defaults:
- Numeric fields: 0 or 0.0
- Boolean fields: False
- Active flags: True

## Installation Process

### After Uninstalling Previous Version:

1. **Manual Upload (Odoo.com)**:
   - Settings > Apps > Import Module
   - Upload `furniture_customization.zip`
   - Install the module

2. **Git Deploy (Odoo.sh)**:
   - Add module to your repository
   - Git push
   - Module auto-installs

## Expected Results

If Odoo.com allows Python code through manual upload:
- ✅ All models created
- ✅ All fields with defaults
- ✅ Computed fields working
- ✅ System parameters set
- ✅ Security rules active

If Odoo.com still blocks Python code:
- ✅ Models and fields created
- ✅ Defaults set
- ❌ Computed fields won't calculate
- ✅ System parameters set
- → Consider moving to Odoo.sh

## Data Loading
After module installation, use the API only for data:
```bash
python3 -m PropertyPortal.erpSetup.loaddata
```

This will:
- Import finish types and finishes
- Import products
- Create product-finish relationships
- NOT create any schema (all in module now)