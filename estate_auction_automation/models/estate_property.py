from odoo import api, fields, models
from odoo.exceptions import UserError


class Estateproperty(models.Model):
    _inherit = 'estate.property'
 
    property_sell_type = fields.Selection([('auction', 'Auction'), ('regular', 'Regular')], string="Selling Type")
    auction_end_time = fields.Datetime(string="End Date")
    state = fields.Selection([
        ('01_template', 'Template'),
        ('02_auction', 'Auction'),
        ('03_sold', 'Sold'),
    ], string='State', copy=False, default='01_template',
        required=True, readonly=False, store=True,
        index=True, tracking=True)

    # relational field
    invoice_ids = fields.One2many(comodel_name='account.move', inverse_name='property_id', string="Invoices")

    # compute fields
    highest_bidder = fields.Many2one(comodel_name='res.partner', compute='_compute_highest_bidder', string="Highest Bidder", copy=False, readonly=True)
    invoice_count = fields.Integer(string="Total Invoices", compute='_compute_invoice_count')

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for invoice in self:
            invoice.invoice_count = len(invoice.invoice_ids)

    @api.depends('offer_ids.price')
    def _compute_highest_bidder(self):
        for property in self:
            highest_offer = max(property.offer_ids, key=lambda offer: offer.price, default=False)
            property.highest_bidder = highest_offer.partner_id if highest_offer else False

    def action_start_property_auction(self):
        """Start the auction if conditions are met."""
        self.ensure_one()
        if self.state != '01_template':
            raise UserError("Only properties in the 'Template' state can start an auction.")
        
        if not self.auction_end_time:
            raise UserError("Please set the auction end time before starting the auction.")

        # Change state to 'Auction'
        self.state = '02_auction'

    @api.model
    def check_auction_over(self):
        """ Scheduled action to auto-accept the highest offer when auction ends. """
        now = fields.Datetime.now()

        # Find properties where auction time has passed but not yet sold
        properties = self.search([
            ('state', '=', '02_auction'),
            ('property_sell_type', '=', 'auction'),
            ('auction_end_time', '<=', now),
            ('stage', 'not in', ['sold', 'cancelled'])
        ])

        for property in properties:
            highest_offer = property.offer_ids.sorted(key=lambda o: o.price,     reverse=True)
            
            if highest_offer:
                highest_offer = highest_offer[0]  # Get the highest bid
                highest_offer.action_accept()  # Accept the highest offer
            
            property.write({
                'state': '03_sold',
                'stage': 'sold'
            })

        return True
