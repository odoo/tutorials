from odoo import fields, models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related='product_template_id.is_kit')
    linked_product_kit_id = fields.Many2one(
        string="Linked product kit Line",
        comodel_name='sale.order.line',
        ondelete='cascade',
        domain="[('order_id', '=', order_id)]",
        copy=False,
        index=True,
    )
    linked_product_kit_ids = fields.One2many(
        string="Linked product kit Lines", comodel_name='sale.order.line', inverse_name='linked_product_kit_id',
    )

    def action_product_kit_wizard(self):
        return {
            'name': 'Add Sub Product',
            'type': 'ir.actions.act_window',
            'res_model': 'subproduct.kit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.order_id.id,
                'default_product_template_id': self.product_template_id.id,
            },
        }
