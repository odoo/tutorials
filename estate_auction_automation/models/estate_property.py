from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    # Property Sale Method
    sale_method = fields.Selection([
        ('auction', "Auction"),
        ('regular', "Regular")
    ], string="Sale Method", copy=False, default='regular')

    auction_deadline = fields.Datetime(string="Auction End Date")

    # Sale State
    state = fields.Selection([
        ('01_template', "Template"),
        ('02_auction', "Auction"),
        ('03_offer_accepted', "Offer Accepted"),
    ], string="Sale State", copy=False, default='01_template',
        required=True, readonly=False, store=True,
        index=True, tracking=True)

    # Related Invoices
    invoice_ids = fields.One2many(comodel_name='account.move', inverse_name='property_id', string="Related Invoices")

    # Computed Fields
    top_bidder = fields.Many2one(
        comodel_name='res.partner',
        compute='_compute_top_bidder',
        string="Top Bidder",
        copy=False,
        readonly=True
    )
    
    @api.depends('offer_ids.price')
    def _compute_top_bidder(self):
        """Computes the top bidder based on the highest offer."""
        for property in self:
            highest_offer = max(property.offer_ids, key=lambda offer: offer.price, default=None)
            property.top_bidder = highest_offer.partner_id if highest_offer else False

    def action_start_auction(self):
        """Starts the auction process if conditions are met."""
        self.ensure_one()

        if self.state != '01_template':
            raise UserError("Auction has already started or ended for this property.")

        if not self.auction_deadline:
            raise UserError("Please specify an auction end date before starting.")

        self.state = '02_auction'

    @api.model
    def _auto_finalize_auctions(self):
        """Scheduled action to finalize auctions when the deadline passes."""
        now = fields.Datetime.now()

        properties = self.search([
            ('state', '=', '02_auction'),
            ('sale_method', '=', 'auction'),
            ('auction_deadline', '<=', now),
            ('status', 'not in', ['offer_accepted', 'sold', 'cancelled'])
        ])

        for property in properties:
            highest_offer = property.offer_ids.sorted(key=lambda o: o.price, reverse=True)

            if highest_offer:
                highest_offer[0].action_accept()
                property.state = '03_offer_accepted'
            else:
                property.state = '01_template'
                property.message_post(body="Auction ended with no offers.")

        return True

    def action_open_invoice(self):
        """ Open Customer Invoices related to this Property """
        invoices = self.env['account.move'].search([('property_id', '=', self.id)])

        if invoices:
            return {
                'name': 'Customer Invoice',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoices.id,
                'context': {'default_move_type': 'out_invoice'},
                'target': 'current',
            }
        else:
            return {'type': 'ir.actions.act_window_close'}
