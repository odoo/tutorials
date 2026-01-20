# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = ['estate.property']

    sale_type = fields.Selection([
        ("regular", "Regular"),
        ("auction", "Auction")
    ], string="Sale Type", default="regular")
    auction_state = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction'),
        ('done', 'Done')
    ],
    string='Auction State', default="template", required=True)
    is_auction_started = fields.Boolean(string="Is Auction Started", default=False)
    is_auction_occured = fields.Boolean(string="Is Auction Occured", default=False)
    auction_duration = fields.Float(string="Auction Duration", default=10000.0) # duration in minutes -> (days=3, hours=3, minutes=33)
    auction_end_datetime = fields.Datetime(string="End Time")
    highest_bidder_id = fields.Many2one("res.partner", string="Highest Bidder", copy=False, readonly=True)
    highest_offer = fields.Float(string="Highest Offer")

    @api.onchange('sale_type')
    def onchange_available_auction(self):
        if(self.sale_type == 'auction' and self.state not in ['new', 'offer_received']):
            raise ValidationError("Auction is only available when propety in 'New' or 'Offer Received' state.")

    def action_toggle_auction(self):
        self.ensure_one()
        self.is_auction_started = not self.is_auction_started
        if (self.is_auction_started):
            self.auction_end_datetime = fields.Datetime().to_string(
                datetime.now() + timedelta(minutes=self.auction_duration))
            self.auction_state = 'auction'
        else:
            self.sale_type = 'regular'
            self.is_auction_occured = True
            self.auction_end_datetime = fields.Datetime().now()
            self.auction_state = 'done'
        return True

    def _track_running_auctions(self):
        running_auctions = self.search([
            ('auction_end_datetime', '>', fields.Datetime.now()),
            ('state', '=', 'offer_received'),
            ('is_auction_started', '=', True)
        ])
        for property in running_auctions:
            highest_offer = property.offer_ids.sorted(lambda record: record.price, reverse=True)[:1]
            if highest_offer:
                print("running")
                property.auction_state = 'auction'
                property.highest_bidder_id = highest_offer.partner_id
                property.highest_offer = highest_offer.price
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
                

    def _auto_accept_highest_offer(self):
        expired_auctions = self.search([
            '|', 
            ('auction_end_datetime', '<', fields.Datetime.now()),
            ('is_auction_occured', '=', True),
            ('state', '=', 'offer_received')
        ])
        for property in expired_auctions:
            property.sale_type = 'regular'
            highest_offer = property.offer_ids.sorted(lambda record: record.price, reverse=True)[:1]
            template = self.env.ref('estate_auction.email_template_auction_result')
            if highest_offer:
                property.write({
                    'auction_state' : 'done',
                    'state' : 'offer_accepted',
                    'selling_price' : highest_offer.price,
                    'buyer_id' : highest_offer.partner_id,
                    'highest_bidder_id' : highest_offer.partner_id
                })
            for offer in property.offer_ids:
                offer.status = 'refused' if offer != highest_offer else 'accepted'
                template.send_mail(offer.id, force_send=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _process_auctions(self):
        """Combine both methods into a single cron job execution."""
        self._track_running_auctions() 
        self._auto_accept_highest_offer()
