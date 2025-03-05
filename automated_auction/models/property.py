from odoo import _, api, fields, models
from odoo.exceptions import UserError


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
        default='regular',
    )
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    highest_offer_bidder = fields.Many2one('res.partner', compute="_compute_highest_bidder", readonly=True)
    auction_state = fields.Selection([
        ('in_template', 'Template'),
        ('in_auction', 'In Auction'),
        ('done', 'Done'),
    ], string='State', copy=False, default='in_template', required=True, tracking=True)

    @api.depends('offer_ids.price')
    def _compute_highest_bidder(self):
        '''compute method to compute highest offer bidder'''
        for record in self:
            highest_offer = max(record.offer_ids, key=lambda o: o.price, default=None)
            record.highest_offer_bidder = highest_offer.partner_id if highest_offer else False

    def action_start_auction(self):
        '''Action Method for start auction'''
        self.ensure_one()
        if not self.end_time:
            raise UserError(_("Please select Auction End Time first"))
        elif self.state in ['sold', 'offer_accepted']:
            raise UserError(_("You can not start auction for offer accepted or sold properties"))
        elif self.auction_state == 'in_auction':
            raise UserError(_("Auction is already going on"))
        self.start_time = fields.Datetime.now()
        self.auction_state = 'in_auction'

    def _auto_accept_property_offer(self):
        '''cron method to check auction ended or not and ended then set values'''
        auction_ended_properties = self.search([
            ('end_time', '<', fields.Datetime.now()),
            ('state', '=', 'offer_received')
        ])
        for property in auction_ended_properties:
            if property.best_price and property.highest_offer_bidder:
                property.write({
                    'buyer_id': property.highest_offer_bidder.id,
                    'selling_price': property.best_price,
                    'state': 'offer_accepted',
                    'auction_state': 'done'
                })
