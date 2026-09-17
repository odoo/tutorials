# Plan: Add `total_area` Computed Field to `estate.property`

## Context
The `estate.property` model currently has `living_area` (Integer) and `garden_area` (Integer) fields but no computed total. The form view displays these fields separately. A `total_area` computed field is needed that sums both.

## Changes

### 1. Model field (`estate/models/estate_property.py`)
- Import `api` from `odoo` (currently only `fields` and `models` are imported).
- Add `total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area", store=True)`.
- Add method `_compute_total_area(self)` decorated with `@api.depends('living_area', 'garden_area')` that sets `total_area = living_area + garden_area`.

### 2. Form view (`estate/views/estate_property_views.xml`)
- Add `<field name="total_area"/>` after `garden_area` in the "Description" page group (matching the pattern shown in the Odoo tutorial goal image).

## Validation
- Verify Python syntax of updated model file.
- Optionally restart Odoo service and upgrade `estate` module to confirm no errors.
