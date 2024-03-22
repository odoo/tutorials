from odoo import Command, exceptions, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def _create_invoices(self):
        if not self.env["account.move"].check_access_rights("create", False):
            try:
                self.check_access_rights("write")
                self.check_access_rule("write")
            except exceptions.AccessError:
                return self.env["account.move"]

        invoice_vals_list = [
            {"name": "6% for selling price", "quantity": 1, "price_unit": 0.06 * self.selling_price},
            {"name": "100 for administration fees", "quantity": 1, "price_unit": 100.}
        ]

        self.ensure_one()

        return self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [Command.create(val) for val in invoice_vals_list],
            "invoice_user_id": self.env.uid,
            "invoice_origin": self.name
        })

    def action_property_sold(self):
        self._create_invoices()
        return super().action_property_sold()
