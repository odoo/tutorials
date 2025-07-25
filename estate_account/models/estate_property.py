from odoo import models
from odoo import Command

class InheritedModel(models.Model):
    _inherit = "estate_property"
    _description = "Estate_Account module"


    def sell(self):
        super().sell()
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        invoice_vals_list = []
        for order in self:
            invoice_vals = {"move_type":"out_invoice", 
                            "partner_id":order.buyer.id, 
                            "journal_id":journal.id,
                            "line_ids": [
                            Command.create({
                                "name":"Downpayment",
                                "price_unit": 0.06*order.selling_price,
                                "quantity":1
                            }),
                            Command.create({
                                 "name":"Admin Fee",
                                "price_unit": 100.0,
                                "quantity":1
                            })
                            ]
                            }
            invoice_vals_list.append(invoice_vals)
        self.env["account.move"].create(invoice_vals_list)
        
        return True

