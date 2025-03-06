from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class EstatePropertyAuction(models.Model):
    _inherit = ["estate.property", "estate.auction.stage.mixin", "estate.property.auction.invoice.mixin"]
    _name = "estate.property"
    _description = "Estate Property Auction"

    sale_type = fields.Selection(
        [("regular", "Regular"), ("auction", "Auction")],
        string="Sale Type",
        required=True,
        default="regular",
    )

    auction_end_time = fields.Datetime(string="Auction End Time", required=False)
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    highest_offer = fields.Monetary(
        string="Highest Offer", readonly=True, currency_field="currency_id"
    )
    highest_bidder = fields.Many2one(
        "res.partner", string="Highest Bidder", readonly=True
    )

    is_auction = fields.Boolean(
        string="Is Auction", compute="_compute_is_auction", store=True
    )

    auction_remaining_time = fields.Char(
        string="Remaining Time", compute="_compute_remaining_time", store=True
    )

    @api.depends("sale_type")
    def _compute_is_auction(self):
        for record in self:
            record.is_auction = record.sale_type == "auction"

    def action_start_auction(self):
        """Start the auction process."""
        for record in self:
            if record.sale_type != "auction":
                raise UserError(_("Only properties marked as 'Auction' can start the auction."))
            if record.auction_stage != "template":
                raise UserError(_("Auction has already been started for this property."))
            if not record.auction_end_time:
                raise UserError(_("You must set an Auction End Time before starting the auction."))
            record.auction_stage = "auction"

    def action_sold(self):
        """Mark the property as sold to the highest bidder."""
        for record in self:
            if record.auction_stage != "auction":
                raise UserError(_("Auction must be in progress before marking as sold."))
            if not record.highest_bidder:
                raise UserError(_("No bids received. Cannot mark as sold."))
            record.auction_stage = "sold"
            record.state = "sold"
            record.buyer_id = record.highest_bidder
            record.selling_price = record.highest_offer
            record.create_invoice()

    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        """Compute the highest offer and set the highest bidder."""
        for record in self:
            highest_offer_value = max(record.offer_ids.mapped("price"), default=0.0)
            highest_bid = record.offer_ids.filtered(lambda o: o.price == highest_offer_value)
            record.highest_offer = highest_offer_value
            record.highest_bidder = highest_bid.partner_id if highest_bid else False

    @api.depends("auction_end_time")
    def _compute_remaining_time(self):
        """Compute the remaining time before the auction ends."""
        for record in self:
            if not record.auction_end_time:
                record.auction_remaining_time = "Auction End Time Not Set"
            else:
                now = fields.Datetime.now()
                remaining_time = record.auction_end_time - now
                if remaining_time.total_seconds() <= 0:
                    record.auction_remaining_time = "Auction Ended"
                else:
                    days = remaining_time.days
                    hours, remainder = divmod(remaining_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    record.auction_remaining_time = (
                        f"{days}d {hours}h {minutes}m {seconds}s left"
                        if days > 0
                        else (
                            f"{hours}h {minutes}m {seconds}s left"
                            if hours > 0
                            else f"{minutes}m {seconds}s left"
                        )
                    )

    def _auto_accept_highest_offer(self):
        """
        Process expired auctions: auto-accept the highest offer and notify all bidders.
        """
        _logger.info("Starting _auto_accept_highest_offer process")
        expired_auctions = self.search([
            ('auction_end_time', '<', fields.Datetime.now()),
            ('auction_stage', '=', 'auction'),
            ('state', 'in', ['new', 'offer_received'])
        ])
        _logger.info("Found %s expired auctions", len(expired_auctions))
        for prop in expired_auctions:
            _logger.info("Processing property ID %s with state '%s' and auction_stage '%s'", prop.id, prop.state, prop.auction_stage)
            # Change sale type to regular to mark the end of the auction process
            prop.sale_type = 'regular'
            highest_offer = prop.offer_ids.sorted(key=lambda r: r.price, reverse=True)[:1]
            # Use the corrected email template external ID (assuming your module is estate_auction)
            template = self.env.ref('estate_auction.mail_template_auction_result')
            if highest_offer:
                highest = highest_offer[0]
                _logger.info("Highest offer for property ID %s is %s from partner %s", prop.id, highest.price, highest.partner_id.id)
                prop.write({
                    'auction_stage': 'sold',
                    'state': 'sold',
                    'selling_price': highest.price,
                    'buyer_id': highest.partner_id.id,
                    'highest_bidder': highest.partner_id.id,
                })
            else:
                _logger.info("No offers found for property ID %s", prop.id)
            for offer in prop.offer_ids:
                offer_status = 'accepted' if highest_offer and offer.id == highest_offer[0].id else 'refused'
                offer.write({'status': offer_status})
                _logger.info("Sending email for offer ID %s: status set to %s", offer.id, offer_status)
                template.send_mail(offer.id, force_send=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _track_running_auctions(self):
        """
        Update or track auctions that are currently running.
        """
        for prop in self.search([('auction_stage', '=', 'auction')]):
            prop._compute_remaining_time()

    def _process_auctions(self):
        """
        Combine auction tracking and finalization into a single cron job execution.
        """
        _logger.info("Starting _process_auctions")
        self._track_running_auctions()
        self._auto_accept_highest_offer()
