from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    sell_type = fields.Selection([
        ('auction', 'Auction'),
        ('regular', 'Regular')
    ])
    stage = fields.Selection([
          ('template', 'Template'),
          ('auction', 'Auction'),
          ('sold', 'Sold'),
        ],
        default='template'
    )
    auction_end_time = fields.Datetime(string="End Date")
    highest_bidder = fields.Many2one(
        'res.partner',
        compute='_compute_highest_bidder',
        string="Highest Bidder",
        copy=False,
        readonly=True,
        store=True
    )
    invoice_ids = fields.One2many(
        'account.move',
        'property_id',
        string="Invoices"
    )
    invoice_count = fields.Integer(string="Invoices", compute='_compute_invoice_count')

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for property in self:
            property.invoice_count = len(property.invoice_ids)

    @api.depends('offer_ids.price')
    def _compute_highest_bidder(self):
        for property in self:
            highest_offer = max(property.offer_ids, key=lambda offer: offer.price, default=None)
            property.highest_bidder = highest_offer.partner_id if highest_offer else False

    def start_property_auction(self):
        for property in self:
            if property.sell_type != 'auction':
                raise exceptions.UserError("Only auction properties can be started.")
            if not property.auction_end_time:
                raise exceptions.UserError("Please set an auction end time before starting the auction.")
            if property.state == 'offer_accepted':
                raise exceptions.UserError("this property has already accepted offer.")
            property.stage = 'auction'

    @api.model
    def check_auction_over(self):
        now = fields.Datetime.now()
        properties = self.search([
            ('stage', '=', 'auction'),
            ('sell_type', '=', 'auction'),
            ('auction_end_time', '<=', now),
            ('state', 'not in', ['sold', 'cancelled'])
        ])
        for property in properties:
            highest_offer = sorted(property.offer_ids, key=lambda offer: offer.price, reverse=True)
            if highest_offer:
                highest_offer = highest_offer[0]
                highest_offer.action_accept()
                property.stage = 'sold'
            else:
                property.stage = 'template'

    def action_open_invoices(self):
      """Open related invoices."""
      self.ensure_one()
      return {
        'name': 'Invoices',
        'type': 'ir.actions.act_window',
        'view_mode': 'list,form',
        'res_model': 'account.move',
        'domain': [('property_id', '=', self.id)],
     }
