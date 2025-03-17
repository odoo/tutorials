from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EstatePropertyAuction(models.Model):
    _inherit = "estate.property"
    _description = "Estate Property Auction"

    sale_type = fields.Selection(
        [("regular", "Regular"), ("auction", "Auction")],
        string="Sale Type",
        required=True,
        default="regular",
    )

    auction_end_time = fields.Datetime(string="Auction End Time")
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
    auction_stage = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction'),
        ('sold', 'Sold'),
    ], string='Auction Stage', default='template')

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
            if record.offer_ids:
                highest_offer = max(record.offer_ids.mapped("price"), default=0.0)
                top_offer = record.offer_ids.filtered(lambda o: o.price == highest_offer)
                record.highest_offer = highest_offer
                record.highest_bidder = top_offer.partner_id if top_offer else False
            else:
                record.highest_offer = 0.0
                record.highest_bidder = False

    @api.depends("auction_end_time")
    def _compute_remaining_time(self):
        """Compute the remaining time before the auction ends."""
        for record in self:
            if not record.auction_end_time:
                record.auction_remaining_time = "Auction End Time Not Set"
            else:
                now = fields.Datetime.now()
                remaining = record.auction_end_time - now
                if remaining.total_seconds() <= 0:
                    record.auction_remaining_time = "Auction Ended"
                else:
                    days = remaining.days
                    hours, rem = divmod(remaining.seconds, 3600)
                    minutes, seconds = divmod(rem, 60)
                    if days > 0:
                        record.auction_remaining_time = f"{days}d {hours}h {minutes}m {seconds}s left"
                    elif hours > 0:
                        record.auction_remaining_time = f"{hours}h {minutes}m {seconds}s left"
                    else:
                        record.auction_remaining_time = f"{minutes}m {seconds}s left"

    def _auto_accept_highest_offer(self):
        """Process expired auctions: auto-accept the highest offer and notify all bidders."""
        _logger.info("Starting _auto_accept_highest_offer process")
        expired = self.search([
            ('auction_end_time', '<', fields.Datetime.now()),
            ('auction_stage', '=', 'auction'),
            ('state', 'in', ['new', 'offer_received']),
        ])
        _logger.info("Found %s expired auctions", len(expired))

        for prop in expired:
            _logger.info(
                "Processing property ID %s with state '%s' and auction_stage '%s'",
                prop.id, prop.state, prop.auction_stage,
            )

            prop.sale_type = 'regular'
            top_offer = prop.offer_ids.sorted(key=lambda r: r.price, reverse=True)[:1]

            template = self.env.ref('estate_auction.mail_template_auction_result', raise_if_not_found=False)

            if top_offer:
                offer = top_offer[0]
                _logger.info(
                    "Highest offer for property ID %s is %s from partner %s",
                    prop.id, offer.price, offer.partner_id.id
                )
                prop.write({
                    'auction_stage': 'sold',
                    'state': 'sold',
                    'selling_price': offer.price,
                    'buyer_id': offer.partner_id.id,
                    'highest_bidder': offer.partner_id.id,
                })
            else:
                _logger.info("No offers found for property ID %s", prop.id)

            for offer in prop.offer_ids:
                is_top = top_offer and offer.id == top_offer[0].id
                offer.write({'status': 'accepted' if is_top else 'refused'})
                _logger.info("Sending email for offer ID %s: status %s", offer.id, offer.status)
                if template:
                    template.send_mail(offer.id, force_send=True)

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def _track_running_auctions(self):
        """Update or track auctions that are currently running."""
        running = self.search([('auction_stage', '=', 'auction')])
        for prop in running:
            prop._compute_remaining_time()

    def _process_auctions(self):
        """Combine auction tracking and finalization into a single cron job execution."""
        _logger.info("Starting _process_auctions")
        self._track_running_auctions()
        self._auto_accept_highest_offer()
