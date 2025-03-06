from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_is_kit = fields.Boolean(related='product_template_id.is_kit', string="Is Kit")
    product_state = fields.Selection(related='order_id.state', string="Product Status")
    kit_parent_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Parent Kit Line",
        help="Main kit product line"
    )

    def unlink(self):
        """Prevent main kit product deletion if sub-products exist, but allow sub-product deletion independently."""
        for line in self:
            if not line.kit_parent_line_id:
                sub_products = self.env['sale.order.line'].search([
                    ('kit_parent_line_id', '=', line.id)
                ])
                if sub_products:
                    raise UserError(
                        """This main kit product has sub-products.
                        Delete them first before deleting the main kit product."""
                    )

        return super(SaleOrderLine, self).unlink()
