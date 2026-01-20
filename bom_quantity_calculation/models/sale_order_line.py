from odoo import models,fields,api,exceptions


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    cust_scheduled_date = fields.Datetime(string="Scheduled Date")

    @api.onchange('cust_scheduled_date')
    def _onchange_cust_scheduled_date(self):
        for line in self:
            if line.cust_scheduled_date and line.order_id.expected_date and line.cust_scheduled_date < line.order_id.expected_date:
                raise exceptions.ValidationError("Schedule date must be greater than or equal to the Expected Date.")
