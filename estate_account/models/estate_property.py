from odoo import api, Command, fields, models


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    state = fields.Selection(
        selection_add =[
            ("invoiced","Invoiced")
        ], ondelete={'invoiced':'cascade'}
    )   

    def action_to_invoice_property(self):
        print("sdfvdfvdfvdfv")
        move_vals = {
            "partner_id": self.partner_id.id,
            "move_type": "out_invoice",
            "date": fields.Date.today(),
            "invoice_origin": self.name,
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": self.name,
                        "price_unit": self.selling_price,
                        "quantity": 1,
                    }
                ),
                Command.create(
                    {
                        "name": "Additional 6%",
                        "price_unit": 0.06 * self.selling_price,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "price_unit": 100,
                    }
                ),
            ],
        }

        self.env["account.move"].create(move_vals)

        res = super(EstateProperty, self).action_property_sold()
        self.state = "invoiced"
        return res
