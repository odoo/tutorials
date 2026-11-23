from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def message_post(self, **kwargs):

        mro = type(self).__mro__
        immediate_parent = mro[mro.index(EstateProperty) + 1]

        res = super(immediate_parent, self).message_post(**kwargs)
        if (
            self.env.context.get("mark_estate_as_sold")
            and self.state == "offer_accepted"
        ):
            self.state = "sold"
            self.env["account.move"].create(
                {
                    "partner_id": self.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6% of the selling price",
                                "quantity": 1,
                                "price_unit": self.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )
        return res
