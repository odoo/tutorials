# Technical Details

This document is a code-oriented reference for the `pharma_control_center` addon.

## Core Models

### `pharmacy.medicine` (`models/pharma_medicine.py`)

Purpose: stores medicine master data, expiry logic, and a simple custom stock quantity.

Notable fields:
- Expiry: `expiry_date`, `days_to_expiry` (computed), `expiry_status` (computed: `fresh` / `expiring_soon` / `expired`)
- Stock: `quantity`, `reorder_level`, `need_reorder` (computed), `in_stock` (computed)
- Pricing: `price`, `cost_price`, `profit_margin` (computed)
- Cart helper: `order_qty` (used by `add_to_cart`)
- Licensing: `license_category` (`green` / `blue` / `white`)
- Sales integration: `product_id` (created on-demand by `_create_product()`)

Key methods:
- `add_to_cart()`: adds the current medicine to the current user’s cart.
- `_create_product()`: creates a `product.product` and links it to the medicine if missing.

Notes:
- `last_sale_order_id` and `last_invoice_id` exist on the model but are currently not updated by any code.

### `pharmacy.cart` and `pharmacy.cart.line` (`models/pharmacy_cart.py`)

Purpose: cart lines + totals + checkout orchestration.

Notable fields (cart):
- `cart_line_ids`: list of cart lines
- `total_quantity`, `total_amount`: computed from cart line subtotals
- `barcode_input`: input field used by `action_add_by_barcode()`
- `interaction_warnings`: computed text summary for interactions among medicines in the cart

Key methods (cart):
- `action_add_by_barcode()`: finds `pharmacy.medicine` by barcode and adds quantity 1.
- `action_add_quick_medicines()`: bulk-adds selected medicines at `quick_order_qty`.
- `action_checkout()`: creates a `sale.order`, creates & posts an invoice, reduces medicine stock, clears the cart.

Drug interaction behavior:
- Warnings are displayed when interactions exist between cart medicines.
- Checkout is blocked only when at least one interaction has `severity == 'severe'`.

### `pharma.control.center` (`models/pharma_control_center.py`)

Purpose: dashboard record + profile sync + computed KPIs.

Profile fields stored on the dashboard:
- `display_name`, `email`, `phone`, `avatar`

Sync behavior:
- On create/write the module syncs profile values to the linked `res.users` and `res.partner`.

Computed KPIs (non-stored):
- Medicine KPIs: totals, stock value, low/out-of-stock, expiring soon, expired
- Patient KPIs: total patients, “my patients” (for doctors)
- Today’s order KPIs: quantity and subtotal for today’s `sale.order.line`

### `pharmacy.patient` (`models/pharmacy_patient.py`)

Purpose: patient data with a required `doctor_id` assignment.

Notable constraints:
- SQL constraint on `email` to keep it unique.

### `pharmacy.interaction` (`models/pharmacy_interaction.py`)

Purpose: defines an interaction between two medicines with `severity` and `warning_text`.

## Checkout Implementation Notes

- The module uses a *custom* stock quantity field (`pharmacy.medicine.quantity`).
- Checkout reduces that field directly (it does not use the Inventory/Stock app).
- The module creates a `product.product` for each medicine on first checkout, and uses that product in `sale.order.line`.
- After order confirmation, the module creates and posts an invoice automatically.

