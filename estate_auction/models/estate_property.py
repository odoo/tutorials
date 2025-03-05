from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    property_selling_type = fields.Selection(
        [('regular', 'Regular'), ('auction', 'Auction')],
        string="Property Type",
        default='regular',
        required=True,
    )
    auction_end_time = fields.Datetime(string="Auction End Time")
    highest_offer = fields.Float(
        string="Highest Offer", readonly=True, compute='_compute_best_offer_and_bidder'
    )
    highest_bidder = fields.Many2one(
        'res.partner',
        string="Highest Bidder",
        readonly=True,
        compute='_compute_best_offer_and_bidder',
    )

    is_auction = fields.Boolean(
        string="Is Auction", compute="_compute_is_auction", readonly=True, store=True, index=True
    )

    auction_stages = fields.Selection(
        [("draft", "Draft"), ("active", "Auction Started"), ("sold", "Sold")], default="draft"
    )

    @api.depends('offer_ids')
    def _compute_best_offer_and_bidder(self):
        for property in self:
            if property.offer_ids:
                best_offer = max(property.offer_ids, key=lambda offer: offer.price)
                property.highest_offer = best_offer.price
                property.highest_bidder = best_offer.partner_id
            else:
                property.highest_offer = 0.0
                property.highest_bidder = False

    @api.depends('property_selling_type')
    def _compute_is_auction(self):
        """Automatically set is_auction based on property_selling_type."""
        for record in self:
            record.is_auction = record.property_selling_type == 'auction'

    def action_estate_auction_start_auction(self):
        if not self.auction_end_time:
            raise UserError("You can't start the auction without defining its end time.")

        if self.auction_end_time <= fields.Datetime.now():
            raise UserError("Auction end time must be in the future.")

        self.auction_stages = "active"

    def automate_auction_property_selling(self):
        properties = self.search([
            ('state', 'in', ('new', 'offer_received')),
            ("is_auction", "=", True),
            ("auction_stages", "=", "active"),
        ])

        for property in properties:
            if not property.auction_end_time or datetime.now() <= property.auction_end_time:
                continue
            best_offer = self.env['estate.property.offer'].search(
                [('property_id', "=", property.id)], order='price desc', limit=1
            )
            if best_offer:
                best_offer.action_estate_property_offer_accept()
                property.auction_stages = "sold"
                property.state = "sold"
            else:
                property.auction_stages = "sold"
                property.state = 'cancelled'
