from odoo import models, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        super().action_sell_property()
        for rec in self:
            if not rec.buyer_id:
                raise UserError(_("Select Buyer Before creating Invoice."))
            self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": rec.buyer_id.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": _("Property Sale: %s") % rec.name,
                                "quantity": 1,
                                "price_unit": (rec.selling_price * 6) / 100,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": _("Administrative fees"),
                                "quantity": 1,
                                "price_unit": 100,
                            },
                        ),
                    ],
                }
            )
