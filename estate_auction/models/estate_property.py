from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    sale_type = fields.Selection(
        [
            ("regular", "Regular Sale"),
            ("auction", "Auction"),
        ],
        default="regular",
        copy=False,
        required=True,
    )
    auction_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("running", "Running"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        copy=False,
    )
    auction_state_color = fields.Integer(compute="_compute_auction_state_color")
    auction_start = fields.Datetime(string="Start Auction From", copy=False)
    auction_end = fields.Datetime(string="End Auction at", copy=False)
    remaining_time = fields.Char(compute="_compute_remaining_time")
    invoice_count = fields.Integer(compute="_compute_invoice_count")
    account_move_ids = fields.One2many(
        "account.move", "estate_property_id", string="Invoices"
    )

    @api.depends("account_move_ids")
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env["account.move"].search_count(
                [
                    ("estate_property_id", "=", record.ids),
                    ("move_type", "=", "out_invoice"),
                ]
            )

    @api.depends("auction_end")
    def _compute_remaining_time(self):
        for record in self:
            if record.auction_end:
                now = fields.Datetime.now()
                diff = record.auction_end - now

                if diff.total_seconds() > 0:
                    total_seconds = int(diff.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    record.remaining_time = "%02dh:%02dm:%02ds" % (
                        hours,
                        minutes,
                        seconds,
                    )
                else:
                    record._cron_check_auction_end()
                    record.remaining_time = "Auction is Ended"
            else:
                record.remaining_time = ""

    def _compute_auction_state_color(self):
        for record in self:
            if record.auction_state == "draft":
                record.auction_state_color = 22
            elif record.auction_state == "running":
                record.auction_state_color = 20
            elif record.auction_state == "done":
                record.auction_state_color = 24
            else:
                record.auction_state_color = 23

    @api.constrains("sale_type", "auction_end")
    def _check_auction_end_required(self):
        for record in self:
            if record.sale_type == "auction" and not record.auction_end:
                raise ValidationError(
                    "Auction end date is required for auction properties."
                )

    def action_start_auction(self):
        for record in self:
            record.auction_state = "running"
            record.auction_start = fields.Datetime.now()

    def action_stop_auction(self):
        for record in self:
            if record.auction_state == "running":
                record.auction_state = "done"

    def action_view_invoices(self):
        self.ensure_one()
        invoices = self.account_move_ids

        if len(invoices) == 1:
            return {
                "name": "Customer Invoice",
                "view_mode": "form",
                "res_model": "account.move",
                "res_id": invoices.id,
                "type": "ir.actions.act_window",
            }
        else:
            return {
                "name": "Customer Invoices",
                "view_mode": "list,form",
                "res_model": "account.move",
                "domain": [("id", "in", invoices.ids)],
                "type": "ir.actions.act_window",
            }

    def action_cancel(self):
        res = super().action_cancel()
        for record in self:
            if record.sale_type == "auction":
                record.auction_state = "cancelled"
        return res

    def action_restore(self):
        res = super().action_restore()
        for record in self:
            if record.sale_type == "auction":
                record.auction_state = "draft"
            else:
                raise UserError("Property is not cancelled.")
        return res

    def action_sold(self):
        res = super().action_sold()
        for record in self:
            if not record.buyer_id:
                raise UserError("Buyer is not set.")

            if not record.selling_price:
                raise UserError("Selling price is not defined.")

            existing = self.env["account.move"].search(
                [
                    ("estate_property_id", "=", record.ids),
                    ("move_type", "=", "out_invoice"),
                ],
                limit=1,
            )
            if existing:
                continue

            income_account = self.env["account.account"].search(
                [("account_type", "=", "income")], limit=1
            )
            commission_amount = record.selling_price * 0.06
            invoice_vals = {
                "move_type": "out_invoice",
                "partner_id": record.buyer_id.id,
                "estate_property_id": record.id,
                "invoice_origin": record.name,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% Commission",
                            "quantity": 1,
                            "price_unit": commission_amount,
                            "account_id": income_account.id,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                            "account_id": income_account.id,
                        }
                    ),
                ],
            }
            self.env["account.move"].create(invoice_vals)
        return res

    def _cron_check_auction_end(self):
        properties = self.env["estate.property"].search(
            [
                ("sale_type", "=", "auction"),
                ("auction_end", "<=", fields.Datetime.now()),
                ("state", "=", "offer_received"),
                ("auction_state", "=", "running"),
            ]
        )
        for property in properties:
            best_offer = property.offer_ids.sorted(key=lambda o: o.price, reverse=True)[
                0
            ]
            best_offer.action_accept_offer()
            property.action_sold()
            property.auction_state = "done"
