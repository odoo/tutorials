from odoo import models, fields, _


class EstatePropertyAuctionInvoiceMixin(models.AbstractModel):
    _name = "estate.property.auction.invoice.mixin"
    _description = "Auction Invoice Mixin"

    invoice_count = fields.Integer(
        string="Invoices",
        compute="_compute_invoice_count",
    )

    def _compute_invoice_count(self):
        """Compute the number of invoices related to the property."""
        for record in self:
            record.invoice_count = record.env["account.move"].search_count([
                ("partner_id", "=", record.buyer_id.id),
                ("move_type", "=", "out_invoice"),
                ("state", "!=", "cancel"),
            ])

    def create_invoice(self):
        """Generate an invoice when the property is sold."""
        for record in self:
            if not record.buyer_id:
                raise ValueError(_("A buyer must be assigned before creating an invoice."))

            invoice_vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [(0, 0, {
                    "name": record.name,
                    "quantity": 1,
                    "price_unit": record.selling_price,
                })],
            }

            invoice = record.env["account.move"].create(invoice_vals)
            record.message_post(
                body=_(
                    "Invoice Created: <a href='/web#id=%(id)s&model=account.move'>%(name)s</a>",
                    {
                        "id": invoice.id,
                        "name": invoice.name,
                    }
                )
            )

    def action_view_invoice(self):
        """Open the invoices related to the property."""
        self.ensure_one()
        invoices = self.env["account.move"].search([
            ("partner_id", "=", self.buyer_id.id),
            ("move_type", "=", "out_invoice"),
            ("state", "!=", "cancel"),
        ])

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [("id", "in", invoices.ids)],
            "context": {"create": False, "default_move_type": "out_invoice"},
            "name": _("Customer Invoices"),
            "view_mode": "list,form",
        }
