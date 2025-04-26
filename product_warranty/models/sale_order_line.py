from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_warranty = fields.Boolean(string="Has Warranty")
    order_line_linked_to_warranty = fields.Many2one(comodel_name="sale.order.line", copy=False , string="Warranty Product", ondelete="cascade")
    is_warranty = fields.Boolean('Is Warranty')

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        for vals in vals_list:
            if vals.get('is_warranty') and not vals.get('order_line_linked_to_warranty'):
                continue
            clean_vals_list.append(vals)
        return super().create(clean_vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        super()._unlink_except_confirmed()
        for line in self:
            if line.is_warranty:
                line.order_line_linked_to_warranty.write({'has_warranty': False})
