from odoo import Command, models
from odoo.exceptions import AccessError
from odoo.tools.translate import _


class EstateModel(models.Model):
    _inherit = "estate.property"

    def _fill_invoice(self, lines):
        self.ensure_one()
        return {
            "move_type": "out_invoice",
            "invoice_user_id": self.env.uid,
            "partner_id": self.buyer_id.id,
            "invoice_origin": self.name,
            "invoice_line_ids": [Command.create(line) for line in lines],
        }

    def _create_invoice_line(self, name, quantity, unit_price):
        return {
            "name": name,
            "quantity": quantity,
            "price_unit": unit_price,
        }

    def _create_invoices(self):
        if not self.env["account.move"].check_access_rights("create", False):
            return self.env["account.move"]

        invoice_vals_list = [
            self._create_invoice_line(f"{self.name} (" + _("6%") + ")", 1, self.selling_price * .06),
            self._create_invoice_line(f"{self.name} (" + _("10 000 before") + ")", 1, 10_1000),
        ]

        return self.env["account.move"].create(self._fill_invoice(invoice_vals_list))


    def action_set_sold(self):
        result = super().action_set_sold()
        self._create_invoices()
        return result
