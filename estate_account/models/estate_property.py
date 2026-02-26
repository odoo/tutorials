from odoo import models, fields, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one("account.move", string="Invoice", copy=False)

    def action_mark_as_sold(self):
        return super().action_mark_as_sold()
