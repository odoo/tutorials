from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=False, domain="[('id', 'in', available_warehouse_ids)]")
    available_warehouse_ids = fields.Many2many('stock.warehouse', compute='_compute_available_warehouses', store=True)
    on_hand_qty_warehouse_wise = fields.Json(string="Available Stocks", compute="_compute_on_hand_qty_warehouse_wise", store=True)
    forecast_qty_warehouse_wise = fields.Json(string="Stocks Forecast", compute="_compute_forecast_qty_warehouse_wise", store=True)

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('product_id')
    def _compute_available_warehouses(self):
        """Compute available warehouses based on the product's primary and secondary warehouse"""

        for line in self:
            if line.product_id and not line.product_id.primary_warehouse_id:
                raise ValidationError("Please add at least Primary warehouse")
            warehouse_ids = []
            if line.product_id.primary_warehouse_id:
                product = line.product_id.product_tmpl_id
                warehouse_ids.append(product.primary_warehouse_id.id)
                if product.secondary_warehouse_id:
                    warehouse_ids.append(product.secondary_warehouse_id.id)
            line.available_warehouse_ids = warehouse_ids

    @api.depends('product_id')
    def _compute_warehouse_id(self):
        """Set the primary warehouse for the product in the order line."""

        for line in self:
            if line.product_template_id and not line.warehouse_id:
                line.warehouse_id = line.product_template_id.primary_warehouse_id

    @api.depends('product_id')
    def _compute_on_hand_qty_warehouse_wise(self):
        """Compute in-hand stock for each warehouse."""

        all_warehouses = self.env['stock.warehouse'].search([])
        for line in self:
            if not line.product_id:
                line.on_hand_qty_warehouse_wise = {}
                continue

            available_data = {}
            for warehouse in all_warehouses:
                stock_qty = sum(self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', 'child_of', warehouse.lot_stock_id.id)
                ]).mapped('quantity'))
                available_data[warehouse.code] = stock_qty

            if not available_data:
                available_data = {"No Stock": 0}

            line.on_hand_qty_warehouse_wise = available_data

    @api.depends('product_id')
    def _compute_forecast_qty_warehouse_wise(self):
        """Compute forecasted stock for each warehouse."""

        all_warehouses = self.env['stock.warehouse'].search([])
        for line in self:
            if not line.product_id:
                line.forecast_qty_warehouse_wise = {}
                continue

            forecast_data = {}
            for warehouse in all_warehouses:
                res = self.env['stock.forecasted_product_product'].with_context(
                    warehouse_id=warehouse.id).get_report_values(docids=line.product_id.ids)
                forecast_data[warehouse.code] = res['docs']['virtual_available']

            if not forecast_data:
                forecast_data = {"No Forecast": 0}
            line.forecast_qty_warehouse_wise = forecast_data
