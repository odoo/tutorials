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
    highest_offer_bidder = fields.Many2one('res.partner', compute='_compute_highest_bidder', readonly=True)
    auction_state = fields.Selection([
        ('in_template', "Template"),
        ('in_auction', "In Auction"),
        ('done', "Done"),
    ], string='State', copy=False, default='in_template', required=True, tracking=True)

    @api.depends('offer_ids.price')
    def _compute_highest_bidder(self):
        '''compute method to compute highest offer bidder'''
        for record in self:
            highest_offer = max(record.offer_ids, key=lambda o: o.price, default=None)
            record.highest_offer_bidder = highest_offer.partner_id if highest_offer else False

    @api.onchange('is_rent_property')
    def _onchange_is_rent_property(self):
        for record in self:
            if record.is_rent_property:
                record.property_auction_type = 'regular'

    def write(self, vals):
        '''Write method to prevent auction state update manually'''
        if self.env.context.get('bypass_write_check'):
            return super().write(vals)

        new_auction_state = vals.get('auction_state')
        if new_auction_state:
            if self.state in ['offer_accepted', 'sold']:
                raise UserError(_("You cannot change the state as the auction has ended"))

            if new_auction_state == 'in_auction':
                self.with_context(bypass_write_check=True).action_start_auction() 
                vals['auction_state'] = new_auction_state
            elif new_auction_state == 'done':
                if self.state == 'new':
                    raise UserError(_("Offer not received yet, you cannot change the state to 'Done'"))
                for offer in self.offer_ids:
                    if offer.price == self.best_price and offer.partner_id == self.highest_offer_bidder:
                        offer.action_accepted()
                        vals['auction_state'] = 'done'
                        break
                self.action_send_mail(self.id)
            elif new_auction_state == 'in_template':
                vals['auction_state'] = 'in_template'
        return super().write(vals)

    def action_start_auction(self):
        '''Action Method for start auction'''
        self.ensure_one()
        if not self.end_time:
            raise UserError(_("Please select Auction End Time first"))
        elif self.state in ['sold', 'offer_accepted']:
            raise UserError(_("You can not start auction for offer accepted or sold properties"))
        elif self.auction_state == 'in_auction':
            raise UserError(_("Auction is already going on"))
        elif self.auction_state == 'done':
            raise UserError(_("Auction ended already"))
        self.with_context(bypass_write_check=True).write({'auction_state': 'in_auction'})

    def _auto_accept_property_offer(self):
        '''cron method to check auction ended or not and ended then set values'''
        auction_ended_properties = self.search([
            ('end_time', '<', fields.Datetime.now()),
            ('state', '=', 'offer_received')
        ])
        for property in auction_ended_properties:
            for offer in property.offer_ids:
                if offer.price == property.best_price and offer.partner_id == property.highest_offer_bidder:
                    offer.action_accepted()
                    property.with_context(bypass_write_check=True).write({'auction_state': 'done'})
                    break
            self.action_send_mail(property.id)

        auction_ended_but_no_offers = self.search([
            ('end_time', '<', fields.Datetime.now()),
            ('state', '=', 'new')
        ])
        for property in auction_ended_but_no_offers:
            property.auction_state = 'in_template'

    def action_send_mail(self, property_id):
        '''method to send mail to the all participants of auction'''
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
