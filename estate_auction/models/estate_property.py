from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    sale_type = fields.Selection(
        [('regular', 'Regular'), ('auction', 'Auction')],
        string="Sale Type",
        default='regular',
        required=True
    )

    auction_end_time = fields.Datetime(string="Auction End Time")
    highest_offer = fields.Float(string="Highest Offer", readonly=True, compute="_compute_highest_offer_bidder")
    highest_bidder = fields.Many2one('res.partner', string="Highest Bidder", readonly=True, compute="_compute_highest_offer_bidder")
    time_left = fields.Char(string="Time Left", compute="_compute_time_left", store=False)
    auction_state = fields.Selection([('normal', 'Template'), ('blocked', 'Auction'), ('done', 'Sold')], default='normal', readonly=True)
    start_time = fields.Datetime(string="Auction Start Time")
    auction_started = fields.Boolean(string="Auction Started", default=False)

    @api.constrains('auction_end_time')
    def _check_end_time(self):
        for record in self:
            if record.auction_end_time and record.auction_end_time < fields.Datetime.now():
                raise ValidationError("End time must be set in the future!")

    @api.depends('offer_ids')
    def _compute_highest_offer_bidder(self):
        for record in self:
            highest_offer = 0
            highest_bidder = False
            for offer in record.offer_ids:
                if offer.price > highest_offer:
                    highest_offer = offer.price
                    highest_bidder = offer.partner_id
            record.highest_offer = highest_offer
            record.highest_bidder = highest_bidder

    @api.depends('auction_end_time')
    def _compute_time_left(self):
        now = fields.Datetime.now()
        for record in self:
            if record.auction_end_time and record.auction_end_time > now:
                diff = record.auction_end_time - now
                total_seconds = int(diff.total_seconds())
                days, remainder = divmod(total_seconds, 86400)
                hours, remainder = divmod(remainder, 3600)
                minutes, seconds = divmod(remainder, 60)
                record.time_left = f"{days}d:{hours}h:{minutes}m:{seconds}s"
            else:
                record.time_left = "Auction Ended"

    def start_auction_action(self):
        for record in self:
            if record.sale_type != 'auction':
                raise UserError("This action can only be used for auction properties.")
            if not record.auction_end_time:
                raise UserError("Please set the Auction End Time before starting the auction.")
            if record.auction_end_time <= fields.Datetime.now():
                raise UserError("End Time must be in the future.")

            record.start_time = fields.Datetime.now()
            record.auction_started = True
            record.auction_state = 'normal'

    def _close_expired_auctions(self):
        now = fields.Datetime.now()
        expired_auctions = self.search([
            ('sale_type', '=', 'auction'),
            ('auction_started', '=', True),
            ('auction_end_time', '<=', now),
        ])
        for property in expired_auctions:
            property.buyer_id = property.highest_bidder
            property.selling_price = property.highest_offer
            property.state = "sold"
            property.auction_state = "done"
            for offer in property.offer_ids:
                if offer.price == property.highest_offer and offer.partner_id == property.highest_bidder:
                    offer.status = "accepted"
                    for record in property.offer_ids:
                        if record.status != "accepted":
                            record.status = "refused"
                    break
            property.action_do_sold()
