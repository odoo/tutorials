from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        # print('create invoiceeeeeeeeee!!!')
        # print(" reached ".center(100, '='))
        # print(self.env.user)
        # print(self.env.user.has_group())
        # self.env['estate.property'].check_access_rights("unlink")
        self.env['account.move'].check_access_rights("write")
        self.env['account.move'].check_access_rule("write")
        invoice_price = {
            "name": self.name,
            "quantity": "1",
            "price_unit": self.selling_price * 0.06,
        }
        administrative_fees = {
            "name": "administrative fees",
            "quantity": "1",
            "price_unit": "100",
        }
        self.env["account.move"].create(
            {
                "name": self.name + " invoice",
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(invoice_price),
                    Command.create(administrative_fees)
                ]
            }
        )
        return self.action_property_cancel()
