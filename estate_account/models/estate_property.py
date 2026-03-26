
from odoo import models


class EstatePropertyModel(models.Model):
    _inherit = "estate.property"



    def action_sold(self):
        res = super().action_sold()
        for record in self:
            invoice_vals = {"partner_id":record.buyer_id.id,"move_type":'out_invoice'}
            self.env['account.move'].create(invoice_vals)
        return res