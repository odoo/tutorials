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
    stage_color = fields.Integer(string="Stage Color", compute="_get_stage_color", store=True)

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
                property.write({
                    'buyer_id': highest_offer.partner_id.id,
                    'selling_price': highest_offer.price,
                    'state': 'sold',
                    'stage': 'sold'
                })
                # Notify the winning bidder
                property.send_auction_result_email(highest_offer.partner_id, "accepted")
                # Notify rejected bidders
                rejected_offers = highest_offer[1:]
                for offer in rejected_offers:
                    property.send_auction_result_email(offer.partner_id, "rejected")

    def send_auction_result_email(self, partner, status):
        """Send email to bidders about auction results."""
        template = self.env.ref('estate.email_template_auction_' + status)
        template.send_mail(self.id, force_send=True)

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

    def _get_stage_color(self):
        """ Assign colors to different stages """
        color_map = {
          'template': 0,  # Grey
          'auction': 2,    # Blue
          'sold': 10       # Green
        }
        for property in self:
           property.stage_color = color_map.get(property.stage, 0)
