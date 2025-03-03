from odoo import api, fields, models


class Property(models.Model):
    _inherit = 'estate.property'

    property_auction_type = fields.Selection(
        string="Auction Type",
        help="Automated auction\n"
             "Regular auction",
        selection=[
            ('auction', "Auction"),
            ('regular', "Regular"),
        ],
        required=True,
        default='auction',
    )
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    highest_offer_amount = fields.Float(readonly=True)
    highest_offer_bidder = fields.Char(readonly=True)
