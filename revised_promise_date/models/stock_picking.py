from odoo import models, fields ,api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    original_promise_date = fields.Date("Original Promise Date" , compute='_compute_original_promise_date')
    sale_order_date = fields.Datetime(related="sale_id.commitment_date", string="Sale Order Date", store=True)
    sale_order_date_only = fields.Date(string="Sale Order Date Only",compute='_compute_order_date_only',store=True)

    @api.depends('sale_id.original_promise_date','date_deadline')
    def _compute_original_promise_date(self):
        """Set the original promise date of stock.picking model with the value of sale.order model's original promise date"""
        for record in self : 
            record.original_promise_date = record.sale_id.original_promise_date

    @api.depends('sale_order_date')
    def _compute_order_date_only(self): 
        """Converts the date_deadline field from datetime to date"""
        for record in self: 
            record.sale_order_date_only = record.sale_order_date.date() if record.sale_order_date else False 
