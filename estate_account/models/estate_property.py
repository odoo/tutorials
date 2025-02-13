from odoo import Command, fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            invoice_vals = {
                "name" : "INV/2025/Test",
                "partner_id" : record.buyer_id.id,
                "move_type" : "out_invoice",
                "invoice_line_ids" : [
                    Command.create({
                        "name" : f"Commission (6%) on {record.name}",
                        "quantity" : 1,
                        "price_unit" : record.selling_price * 0.06
                    }),
                    Command.create({
                        "name" : "Administrative Fees",
                        "quantity" : 1,
                        "price_unit" : 100
                    }),
                ]
            }
            invoice = record.env["account.move"].create(invoice_vals)
        return super().action_sold()
