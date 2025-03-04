from odoo import fields, models


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
    auction_highest_offer = fields.Integer("Highest Offer")
    auction_highest_bidder = fields.Many2one('res.partner', "Highest Bidder")

    def start_auction(self):
        pass
