from odoo import Command, _, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one("account.move", string="Invoice", copy=False)

    def action_mark_as_sold(self):
        res = super().action_mark_as_sold()
        for property_rec in self:
            if not property_rec.buyer_id:
                raise UserError(_("No buyer defined. May be NO Offer is accepted"))
            journal = self.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            )
            commission = property_rec.selling_price * 0.06
            admin_fee = 100.0
            invoice_lines = [
                Command.create(
                    {
                        "name": "Commission 6%",
                        "quantity": 1,
                        "price_unit": commission,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fee",
                        "quantity": 1,
                        "price_unit": admin_fee,
                    }
                ),
            ]
            invoice_vals = {
                "partner_id": property_rec.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_origin": property_rec.name,
                "invoice_line_ids": invoice_lines,
            }
            invoice = self.env["account.move"].sudo().create(invoice_vals)
            property_rec.invoice_id = invoice.id
        return res
