from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_warranty = fields.Boolean(string="Has Warranty")
    order_line_linked_to_warranty = fields.Many2one(comodel_name="sale.order.line", copy=False, string="Warranty Product", ondelete="cascade")
    is_warranty = fields.Boolean('Is Warranty')

    @api.constrains('product_uom_qty')
    def _check_warranty_qty_limit(self):
        for line in self:
            if line.is_warranty and line.order_line_linked_to_warranty:
                linked_line = line.order_line_linked_to_warranty
                print(f"Checking warranty quantity: {line.product_uom_qty} > linked product quantity: {linked_line.product_uom_qty}")
                if line.product_uom_qty > linked_line.product_uom_qty:
                    raise ValidationError(
                        f"The warranty quantity ({line.product_uom_qty}) cannot be more than the linked product quantity ({linked_line.product_uom_qty})."
                    )

            elif not line.is_warranty:
                warranty_line = self.search([
                    ('order_line_linked_to_warranty', '=', line.id),
                    ('is_warranty', '=', True)
                ], limit=1)

                if warranty_line:
                    if line.product_uom_qty < warranty_line.product_uom_qty:
                        raise ValidationError(
                            f"The quantity of the product ({line.product_uom_qty}) cannot be less than the linked warranty quantity ({warranty_line.product_uom_qty})."
                        )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        super()._unlink_except_confirmed()
        for line in self:
            if line.is_warranty:
                line.order_line_linked_to_warranty.write({'has_warranty': False})
