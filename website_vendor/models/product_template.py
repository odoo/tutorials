from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_price = fields.Float(
        string="Minimum Price",
        compute='_compute_min_price',
        store=True,
        readonly=True
    )

    max_price = fields.Float(
        string="Maximum Price",
        compute='_compute_max_price',
        store=True,
        readonly=True
    )

    
    @api.depends('seller_ids', 'seller_ids.price', 'seller_ids.min_qty')
    def _compute_min_price(self):
        for product in self:
            prices = [
                seller.price / (seller.min_qty or 1)
                for seller in product.seller_ids if seller.price > 0
            ]
            product.min_price = min(prices) if prices else 0.0


    @api.depends('seller_ids', 'seller_ids.price', 'seller_ids.min_qty')
    def _compute_max_price(self):
        for product in self:
            prices = [
                seller.price / (seller.min_qty or 1)
                for seller in product.seller_ids if seller.price > 0
            ]
            product.max_price = max(prices) if prices else 0.0
