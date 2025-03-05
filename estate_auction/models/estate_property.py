from odoo import api, fields, models
from datetime import datetime

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    selling_type = fields.Selection(
        selection = [
            ('auction', "Auction"),
            ('regular', "Regular")
        ],
        default='regular'
    )

    auction_state = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction'),
        ('sold', 'Sold')
    ],
    string='Auction State',
    default='template',
    required=True
    )

    auction_end_date = fields.Datetime("End Date")
    auction_highest_offer = fields.Integer("Highest Offer", compute="_compute_highest_offer")
    auction_highest_bidder = fields.Many2one('res.partner', "Highest Bidder", compute="_compute_highest_offer")

    @api.depends('offer_ids')
    def _compute_highest_offer(self):
        for record in self:
            if record.offer_ids:
                highest_offer = max(record.offer_ids, key=lambda offer:offer.price)
                record.auction_highest_offer = highest_offer.price
                record.auction_highest_bidder = highest_offer.partner_id
            else:
                record.auction_highest_offer = 0
                record.auction_highest_bidder = None

    def _check_auction_status(self):
        properties = self.search([('selling_type', '=', 'auction'), ('auction_state', '=', 'auction'), ('state', 'in', ['new', 'offer_received'])])
        for property in properties:
            if(datetime.now() > property.auction_end_date):
                highest_offer = max(property.offer_ids, key=lambda offer:offer.price)
                for offer in property.offer_ids:
                    if offer != highest_offer:
                        offer.status = 'refused'

                property.write({
                    'auction_state' : 'sold',
                    'buyer_id' : highest_offer.partner_id,
                    'selling_price' : highest_offer.price,
                    'state' : 'offer_accepted'
                })
                highest_offer.status = 'accepted'
                
    def start_auction(self):
        for record in self:
            record.auction_state = 'auction'
