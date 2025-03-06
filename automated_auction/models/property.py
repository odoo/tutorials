from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _inherit = 'estate.property'

    property_auction_type = fields.Selection(
        string="Auction Type",
        help="Automated auction\nRegular auction",
        selection=[
            ('auction', "Auction"),
            ('regular', "Regular"),
        ],
        required=True,
        default='regular',
    )
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
        self.auction_state = 'in_auction'

    def _auto_accept_property_offer(self):
        '''cron method to check auction ended or not and ended then set values'''
        auction_ended_properties = self.search([
            ('end_time', '<', fields.Datetime.now()),
            ('state', '=', 'offer_received')
        ])
        for property in auction_ended_properties:
            for offer in property.offer_ids:
                offer.action_accepted()
            if property.best_price and property.highest_offer_bidder:
                property.write({
                    'buyer_id': property.highest_offer_bidder.id,
                    'selling_price': property.best_price,
                    'auction_state': 'done'
                })
                self.action_send_mail(property.id)
        if not auction_ended_properties:
            auction_ended_but_no_offers = self.search([
                ('end_time', '<', fields.Datetime.now()),
                ('state', '=', 'new')
            ])
            for property in auction_ended_but_no_offers:
                property.write({'auction_state': 'done'})

    def action_send_mail(self, property_id):
        property = self.env['estate.property'].browse(property_id)
        
        offer_accepted_participant = property.highest_offer_bidder
        offer_refused = self.env['estate.property.offer'].search([
            ('property_id', '=', property_id),
            ('status', '=', 'refused')
        ])

        template_offer_accepted = self.env.ref('automated_auction.email_template_for_offer_accepted')
        template_offer_refused = self.env.ref('automated_auction.email_template_for_offer_refused')

        if offer_accepted_participant:
            template_offer_accepted.send_mail(property_id, force_send=True)
        for offer in offer_refused:
            template_offer_refused.send_mail(offer.id, force_send=True)
