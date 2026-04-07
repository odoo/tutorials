from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    sale_type = fields.Selection(
        [("regular", "Regular Sale"), ("auction", "Auction")],
        default="regular",
        required=True,
    )
    auction_end_time = fields.Datetime()
    state = fields.Selection(selection_add=[("template", "Template"), ("auction", "Auction")])
    invoice_ids = fields.One2many("account.move", "property_id", string="Invoices")
    invoice_count = fields.Integer(compute="_compute_invoice_count", string="Number of Invoices")

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    @api.constrains('sale_type', 'auction_end_time', 'state')
    def _check_auction_end_time(self):
        auction_records = self.filtered_domain([('sale_type', '=', "auction")])
        if not auction_records:
            return

        if auction_records.filtered_domain([('auction_end_time', '=', False)]):
            raise ValidationError(_("Auction end time is required for auction properties."))

        active_auction_records = auction_records.filtered_domain([('state', '=', "auction")])
        if active_auction_records.filtered_domain([('auction_end_time', '<=', fields.Datetime.now())]):
            raise ValidationError(_("Auction end time must be in the future."))

    def _create_property_invoice(self):
        self.ensure_one()
        if self.invoice_ids:
            return self.invoice_ids[0]
        if not self.buyer_id:
            raise ValidationError(_("A buyer is required before creating an invoice."))

        return self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "property_id": self.id,
                "line_ids": [
                    Command.create(
                        {
                            "name": "selling price addons (6%)",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        },
                    ),
                ],
            },
        )

    @api.model
    def _cron_process_expired_auctions(self):
        expired_auctions = self.search([
            ('sale_type', '=', "auction"),
            ('state', '=', "auction"),
            ('auction_end_time', '<=', fields.Datetime.now()),
        ])

        for prop in expired_auctions:
            valid_offers = prop.offer_ids.filtered_domain([
                ('is_auction_bid', '=', True),
                ('status', '!=', "refused"),
            ])
            if not valid_offers:
                prop.state = "template"
                continue

            if "accepted" not in valid_offers.mapped("status"):
                winning_offer = valid_offers.sorted("price", reverse=True)[0]
                if winning_offer:
                    winning_offer.action_accept()
            prop.action_sold()

    def action_start_auction(self):
        if self.filtered_domain([('sale_type', '!=', "auction")]):
            raise ValidationError(_("Only properties in Auction mode can start an auction."))
        if self.filtered_domain([('state', '=', 'auction')]):
            raise ValidationError(_("Auction is already running for this property."))
        if self.filtered_domain([('state', 'in', ["sold", "canceled", "offer_accepted"])]):
            raise ValidationError(_("You cannot start an auction for sold, canceled, or accepted properties."))
        if self.filtered_domain([('auction_end_time', '=', False)]):
            raise ValidationError(_("Please set an auction end time before starting the auction."))
        if self.filtered_domain([('auction_end_time', '<=', fields.Datetime.now())]):
            raise ValidationError(_("Auction end time must be in the future."))

        self.write({'state': 'auction'})
        return True

    def action_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError(_("Canceled properties cannot be sold."))

        self._create_property_invoice()
        result = super().action_sold()
        if self.sale_type == "auction":
            self.message_post(
                body=_(
                    "Auction finalized. Winning bid: %(amount)s from %(partner)s.",
                    amount=self.selling_price,
                    partner=self.buyer_id.name,
                ),
            )
        return result

    def action_view_invoice(self):
        self.ensure_one()
        if not self.invoice_ids:
            return False

        return {
            "type": "ir.actions.act_window",
            "name": _("Invoice"),
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.invoice_ids[0].id,
        }
