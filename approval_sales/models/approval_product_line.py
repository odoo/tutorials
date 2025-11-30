# Part of Odoo. See LICENSE file for full copyright and licensing details.

from markupsafe import Markup

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ApprovalProductLine(models.Model):
    _name = 'approval.product.line'
    _inherit = ['approval.product.line', 'mail.thread']

    unit_price = fields.Float(string="Unit Price")
    cost_price = fields.Float(string="Cost Price")
    margin = fields.Float(string="Margin", compute='_compute_margin', inverse='_inverse_margin')
    custom_margin = fields.Float(string="Custom Margin")
    final_price = fields.Float(string='final price', compute='_compute_final_price', inverse='_inverse_final_price', store=True)
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line", string="Sale Order Line Id")

    @api.depends('custom_margin', 'quantity', 'cost_price')
    def _compute_final_price(self):
        for record in self:
            final_price = record.quantity * ((record.custom_margin / 100 * record.cost_price) + record.cost_price) if record.cost_price else 0
            if round(record.final_price, 2) != round(final_price, 2):
                record.final_price = final_price

    def _inverse_final_price(self):
        for record in self:
            custom_margin = (record.final_price - record.cost_price) / record.cost_price * 100 if record.cost_price else 0
            if round(record.custom_margin, 2) != round(custom_margin, 2):
                record.custom_margin = custom_margin

    @api.depends('unit_price', 'cost_price')
    def _compute_margin(self):
        for record in self:
            record.margin = ((record.unit_price - record.cost_price) / record.cost_price) * 100 if record.cost_price else 0

    def _inverse_margin(self):
        for record in self:
            record.unit_price = record.cost_price * (1 + record.margin / 100)

    def write(self, vals):
        for record in self:
            if 'cost_price' in vals and vals['cost_price'] <= 0:
                raise ValidationError(_("Cost Price must be strictly positive."))
            old_custom_margin = record.custom_margin
            old_final_price = record.final_price
            res = super().write(vals)
            msg = [f"<b>• {record.product_id.name}:</b> <br>"]
            if old_custom_margin != record.custom_margin and old_final_price != record.final_price:
                msg.append(f"<i>Custom Margin:</i> {old_custom_margin:.2f} → {record.custom_margin:.2f}<br>")
            if old_final_price != record.final_price:
                msg.append(f"<i>Final Price:</i> {old_final_price:.2f} → {record.final_price:.2f}<br>")
            if len(msg) > 1:
                record.approval_request_id.message_post(
                    body=Markup(" ".join(msg)),
                    message_type="notification",
                )
        return res
