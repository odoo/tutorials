from odoo import api, fields, models


class KitSubProductLineWizard(models.TransientModel):
    _name = 'kit.sub.product.line.wizard'
    _description = 'this is used for sub products line'

    _sql_constraints = [
        ('sub_product_price_check', 'CHECK(price >= 0)', 'price must be positive'),
        ('quantity_check', 'CHECK(quantity >= 1)', 'quantity should be atleast 1')
    ]

    parent_wizard_id = fields.Many2one('kit.add.sub.products.wizard')
    sub_product_id = fields.Many2one('product.product', string='product', ondelete="cascade")
    quantity =  fields.Float(default=1.0)
    price = fields.Float(string='Unit price')
    order_line_id = fields.Many2one('sale.order.line', ondelete="cascade")

    @api.onchange('sub_product_id')
    def _onchange_sub_product_price(self):
        for sub_product in self:
            sub_product.price = sub_product.sub_product_id.lst_price
