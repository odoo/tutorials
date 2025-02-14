from odoo import models, api, fields
class EstateProperty(models.Model):
    _inherit = "estate.property"

    #------------------------------------------Action Methods----------------------------------------------
    def property_sold_action(self):
        """set property state as sold and Create invoice for sold property"""
        res = super().property_sold_action()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for property in self:
            self.env["account.move"].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                "journal_id": journal.id,
                'invoice_date': fields.Date.today(),
                "invoice_line_ids": [
                    (0,0,{
                            "name": property.name,
                            "quantity": 1.0,
                            "price_unit": property.selling_price * 6.0 / 100.0,
                        },
                    ),
                    (0,0,
                        {
                            "name": "Administrative fees",
                            "quantity": 1.0,
                            "price_unit": 100.0,
                        },
                    ),
                ]
            })
            return res
