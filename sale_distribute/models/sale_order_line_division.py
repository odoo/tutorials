from odoo import api, fields, models


class SaleOrderLineDivision(models.Model):
    _name = "sale.order.line.division"
    _description = "Sale Order Line Division"

    amount = fields.Float(string="Amount", required=True)

    @api.depends('amount')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.amount:.2f}"
