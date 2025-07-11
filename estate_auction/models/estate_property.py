from odoo import fields, models, api
from datetime import timedelta


class estate_property(models.Model):
    _inherit = "estate.property"

    selling_type = fields.Selection([
        ('auction', 'Auction'),
        ('regular', 'Regular')
    ], string=' ', default='regular')
    end_time = fields.Datetime(string="End Time: ")
    highest_offer = fields.Float(string="Highest Offer: ", readonly=True, compute="_compute_highest_offer")
    highest_bidder = fields.Many2one("res.partner", readonly=True, compute="_compute_highest_bidder")
    auction_state = fields.Selection([('normal', 'Template'), ('blocked', 'Auction'), ('done', 'Sold')], default='normal', readonly=True)
    time_remaining = fields.Char(string="Time Remaining", compute="_compute_time_remaining", readonly=True)
    lock_selling_type = fields.Boolean(string='Lock Selling Type')

    @api.onchange('end_time')
    def _check_end_time(self):
        for record in self:
            if record.end_time < fields.Datetime.now():
                raise models.ValidationError("You can't end the auction before now.")

    def _close_expired_auctions(self):
        now = fields.Datetime.now()
        expired_properties = ""
        expired_properties = self.search([
            ('selling_type', '=', 'auction'),
            ('end_time', '<=', now),
            ('auction_state', 'in', ['blocked'])
        ])
        for property in expired_properties:
            property.buyer_id = property.highest_bidder
            property.selling_price = property.highest_offer
            property.status = "sold"
            property.auction_state = "done"
            for offer in property.offer_ids:
                if offer.price == property.highest_offer and offer.partner_id == property.highest_bidder:
                    offer.status = "accepted"
                    for record in property.offer_ids:
                        if record.status not in "accepted":
                            record.status = "refused"

    @api.depends('end_time')
    def _compute_time_remaining(self):
        for record in self:
            if record.end_time:
                now = fields.Datetime.now()
                remaining = record.end_time - now
                if remaining.total_seconds() > 0:
                    hours, remainder = divmod(int(remaining.total_seconds()), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    record.time_remaining = f" Auction ends in: {hours:02d}h {minutes:02d}m {seconds:02d}s"
                else:
                    record.time_remaining = "Auction Ended"
            else:
                record.time_remaining = "It has not started yet."

    def action_start_auction(self):
        for property in self:
            if not property.end_time:
                property.end_time = fields.Datetime.now() + timedelta(days=2)
                property.auction_state = 'blocked'

            if property.end_time:
                property.lock_selling_type = True
            else:
                property.lock_selling_type = False

    @api.depends('offer_ids.price')
    def _compute_highest_offer(self):
        for record in self:
            record.highest_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.depends('offer_ids.price')
    def _compute_highest_bidder(self):
        for record in self:
            record.highest_bidder = ""
            if record.offer_ids:
                for offer in record.offer_ids:
                    if offer.price == max(record.offer_ids.mapped('price'), default=0):
                        record.highest_bidder = offer.partner_id
                        break
