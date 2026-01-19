from odoo import models, Command, exceptions, _


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError(_("Properties which are Cancelled cannot be Sold"))

            admin_fee = record.salesperson.sales_fee if record.salesperson else 500

            self.env["account.move"].create({
                "partner_id": record.customer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.6,
                    }),
                    Command.create({
                        "name": _("Administrative fees"),
                        "quantity": 1,
                        "price_unit": admin_fee,
                    }),
                ],
            })

        return super().action_sold_property()
