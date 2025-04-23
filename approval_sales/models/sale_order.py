# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_status = fields.Selection(
        string="Approval Status",
        related='approval_id.request_status',
        copy=False,
        tracking=True)
    approval_id = fields.Many2one(comodel_name="approval.request", string="Approval", copy=False)

    def action_open_approval_request(self):
        return {
            'name': "My Requests",
            'type': 'ir.actions.act_window',
            'res_model': 'approval.request',
            'view_mode': 'form',
            'res_id': self.approval_id.id,
            'target': 'current',
        }

    def action_create_approval(self):
        self.ensure_one()
        categ_id = self.env['approval.category'].search([('approval_type', '=', 'sales')])

        cp_less_products = list()
        for line in self.order_line:
            if not line.product_id.standard_price:
                cp_less_products.append(line.product_id.name)
        if cp_less_products:
            raise ValidationError(_(f"Cost Price of {', '.join(cp_less_products)} is not set."))

        approval_vals = {
            'request_owner_id': self.env.user.id,
            'category_id': categ_id.id,
            'request_status': 'pending',
            'sale_order_id': self.id,
        }
        approval = self.env["approval.request"].create(approval_vals)
        self.approval_id = approval.id
        product_line = self.env["approval.product.line"]

        for line in self.order_line:
            product_line_vals = {
                'approval_request_id': approval.id,
                'product_id': line.product_id.id,
                'quantity': 1,
                'unit_price': line.price_unit,
                'cost_price': line.product_id.standard_price,
                'margin': (line.price_unit - line.product_id.standard_price) / line.product_id.standard_price * 100,
                'custom_margin': (line.price_unit - line.product_id.standard_price) / line.product_id.standard_price * 100,
                'sale_order_line_id': line.id,
            }
            product_line.create(product_line_vals)
        return True
