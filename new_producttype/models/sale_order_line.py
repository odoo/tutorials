from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(string='Is kit', related='product_id.is_kit')
    parent_line_id = fields.Many2one("sale.order.line", ondelete="cascade")
    sub_products_ids = fields.Many2many(
        "product.product",
        related="product_template_id.sub_products_ids",
        string="Sub Products",
    )

    def action_open_kit_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'sub.product.kit.wizard.view',
            'res_model': 'sub.product.kit.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
