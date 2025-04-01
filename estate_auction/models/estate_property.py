from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property' 

    auction_end_time = fields.Date(string="Auction End Date", copy=False)
    is_auction_started = fields.Boolean(compute="set_is_auction_ended", default=False)
    # auction_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers", tracking=True)
    bid_type=fields.Selection(
        [('auction', 'Auction'),('regular', 'Regular')],
        string=" Bid Type",
        default='auction',
        copy=False,
        tracking=True
    )
    auction_status=fields.Selection(
        [('auction_not_begun', 'Auction Not Started'),('auction_started', 'Auction Started'), ('auction_ended', 'Auction Ended')],
        string=" Auction Status",
        default='auction_not_begun',
        readonly=True,
        copy=False,
        tracking=True
    )
    highest_offer = fields.Float(string="Highest Offer", compute="_compute_highest_offer", readonly=True)
    highest_bidder = fields.Many2one("res.partner", string="Highest Bidder", readonly=True)

    # _sql_constraints = [
    #     ('check_offer_price', 'CHECK(offer_price >= expected_price )', 'The offer price should be p greater than expected price.'),
    # ]

    def start_auction(self):
        if not self.is_auction_started:
            self.auction_end_time = fields.Datetime.now() + timedelta(days=10)
            self.is_auction_started = True
            self.highest_offer = 0.0
            self.highest_bidder = False
            self.auction_status = "auction_started"
            print("Start Auction pressed: ", self.auction_end_time)

    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        for record in self:
            record.highest_offer = max(record.mapped('offer_ids.price'), default=0)
            highest_bid_offer_id = record.offer_ids.filtered(lambda o: o.price == record.highest_offer)
            record.highest_bidder = highest_bid_offer_id.partner_id

    @api.depends('auction_end_time')
    def set_is_auction_ended(self):
        if self.is_auction_started and self.auction_end_time < datetime.now():
            self.selling_price=self.highest_offer
            self.auction_status="auction_ended"
            self.is_auction_started = False
            self.status="offer_accepted"

    
