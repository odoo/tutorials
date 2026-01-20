from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EstatePropertyAuction(models.Model):
    _inherit = 'estate.property'

    sale_type = fields.Selection(
        [
            ('auction', 'Auction'),
            ('regular', 'Regular')
        ],
        string="Sale Type", default="regular"
    )
    auction_state = fields.Selection(
        [
            ('template', 'Auction'),
            ('auction', 'Auction Started'),
            ('sold', 'Sold'),
        ],
        string="Auction Status", default="template", tracking=True
    )
    auction_endtime = fields.Datetime(string="End time")
    highest_offer = fields.Float(string="Highest Offer", readonly=True)
    highest_bidder = fields.Char(string="Highest Bidder", readonly=True)
    timer_running = fields.Boolean(string="Timer", default=False)

    @api.depends('auction_endtime')
    def _check_auction_endtime(self):
        for record in self:
            if record.auction_endtime and record.auction_endtime <= datetime.now():
                raise ValidationError(_("You can only select a date from tomorrow onwards."))

    @api.onchange('sale_type')
    def _onchange_sale_type(self):
        for record in self:
            if self.sale_type == 'regular':
                self.auction_endtime = ""

    def action_auction_start_button(self):
        if not self.auction_endtime:
            raise UserError(_('End time cannot be empty. Please enter a value.'))
        else:
            self.auction_state = 'auction'
            self.timer_running = True

    def action_cancel_button(self):
        result = super().action_cancel_button()
        for record in self:
            record.timer_running = False
        return result

    def action_sold_button(self):
        result = super().action_sold_button()
        for record in self:
            record.auction_state = 'sold'
        return result

    def offer_status_send_email(self):
        for record in self:
            offers = self.env['estate.property.offer'].search([('property_id', '=', record.id)])
            best_offer = max(offers, key=lambda offer: offer.price, default=None)

            for offer in offers:
                if best_offer and offer.id == best_offer.id:
                    offer.action_offer_accept_button()
                    record.highest_bidder = offer.partner_id.name
                    record.highest_offer = offer.price
                    template = self.env.ref('estate_auction.email_template_offer_accepted', raise_if_not_found=False)
                else:
                    offer.action_offer_refuse_button()
                    template = self.env.ref('estate_auction.email_template_offer_rejected', raise_if_not_found=False)

                if template:
                    template.send_mail(offer.id, force_send=True)

    @api.model
    def _check_auction_time_status(self):
        properties = self.search([('timer_running', '=', True), ('auction_endtime', '<=', datetime.now())])
        for property in properties:
            property.timer_running = False
            property.offer_status_send_email()
