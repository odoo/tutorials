from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        params = self.env["ir.config_parameter"].sudo()

        if params.get_str("estate_account.commission_rate") is None:
            params.set_float("estate_account.commission_rate", 0.06)
        if params.get_str("estate_account.administrative_fee") is None:
            params.set_float("estate_account.administrative_fee", 100.0)

        commission_rate = params.get_float(
            "estate_account.commission_rate", default=0.06
        )
        administrative_fee = params.get_float(
            "estate_account.administrative_fee", default=100.0
        )

        invoice_list = []
        for record in self:
            if not record.buyer_id:
                raise UserError(
                    self.env._(
                        "A buyer must be set before creating an invoice for a sold property."
                    )
                )
            invoice = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": record.name,
                            "quantity": 1,
                            "price_unit": record.selling_price * commission_rate,
                        }
                    ),
                    Command.create(
                        {
                            "name": self.env._("Administrative Fees"),
                            "quantity": 1,
                            "price_unit": administrative_fee,
                        }
                    ),
                ],
            }
            invoice_list.append(invoice)

        self.env["account.move"].create(invoice_list)
        return res
