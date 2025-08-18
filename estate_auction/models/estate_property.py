from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    auction_state = fields.Selection(
        [('01_template', 'Template'), ('02_auction', 'Auction'), ('03_sold', 'Sold')],
        string='Auction State',
        copy=False,
        default='01_template',
        required=True,
        readonly=True,
    )
    sale_mode = fields.Selection(
        [('auction', 'Auction'), ('regular', 'Regular')],
        string='Sale Mode',
        default='regular',
        required=True,
    )
    auction_end_time = fields.Datetime(
        string='End Time', default=(relativedelta(days=7) + datetime.today()).replace(second=0, microsecond=0)
    )
    highest_bidder_id = fields.Many2one(
        'res.partner',
        string='Highest Bidder',
        compute='_compute_highest_bid',
        store=True,
        default=False,
    )
    highest_offer = fields.Float(
        'Highest Offer', compute='_compute_highest_bid', store=True, default=0
    )

    @api.depends('offer_ids')
    def _compute_highest_bid(self):
        for record in self:
            if record.sale_mode != 'auction':
                continue
            if not record.offer_ids:
                record.highest_bidder_id = False
                record.highest_offer = 0.0
                continue
            max_offer = max(record.offer_ids, key=lambda x: x.price, default=None)
            if max_offer is not None:
                record.highest_bidder_id = max_offer.partner_id.id
                record.highest_offer = max_offer.price

    def action_start_estate_auction(self):
        if not self.auction_end_time:
            raise UserError("You can't start the auction without defining end time.")

        if self.auction_end_time <= datetime.now():
            raise UserError('Auction end time must be in the future.')

        self.auction_state = '02_auction'

    def automate_auction_sales(self):
        properties = self.search([
            ('state', 'in', ('new', 'offer_received')),
            ('sale_mode', '=', 'auction'),
            ('auction_state', '=', '02_auction'),
        ])

        for estate in properties:
            if not estate.auction_end_time or datetime.now() <= estate.auction_end_time:
                continue

            best_offer = self.env['estate.property.offer'].search(
                [('property_id', '=', estate.id)],
                order='price desc, create_date asc',
                limit=1,
            )
            if best_offer:
                best_offer.action_accept()
                estate.auction_state = '03_sold'
                estate.action_sold()
            else:
                estate.auction_state = '03_sold'
                estate.state = 'cancelled'
