from odoo import fields, models


class SubProductKitWizard(models.TransientModel):
    _name = 'sub.product.kit.wizard'

    sale_order_line_id = fields.Many2one('sale.order.line')
    sub_products_ids = fields.One2many('sub.product.line.kit.wizard', 'sub_products_line_id')

    def action_confirm(self):
        pass
