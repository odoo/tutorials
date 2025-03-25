# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    has_sale_quantity = fields.Selection(related="category_id.has_sale_quantity", string="Has Sale Quantity")
    has_sale_product = fields.Selection(related="category_id.has_sale_product", string="Has Sale Product")
    has_unit_price = fields.Selection(related="category_id.has_unit_price", string="Has Unit Price")
    has_cost_price = fields.Selection(related="category_id.has_cost_price", string="Has Cost price")
    has_margin = fields.Selection(related="category_id.has_margin", string="Has Margin")
    has_margin_custom = fields.Selection(related="category_id.has_margin_custom", string="Has Margin Custom")
    has_final_price = fields.Selection(related="category_id.has_final_price", string="Has Final Price")
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    sale_order_count = fields.Integer(string="Sale order Count", compute="_compute_sale_order_count")
    is_final_price_sent = fields.Boolean(string="Is Final Price Sent")

    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = self.env['sale.order'].search_count([('id', '=', record.sale_order_id.id)])

    def action_open_sale_order(self):
        return {
            'name': "Quotations",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
            'target': 'current',
        }

    def action_submit_final_price(self):
        if self.request_status == 'approved':
            self.sale_order_id.update({'approval_status': 'approved'})
            self.is_final_price_sent = True
            for line in self.product_line_ids:
                if line.unit_price != line.final_price:
                    line.sale_order_line_id.update({'price_unit': line.final_price / line.quantity})
        return True
