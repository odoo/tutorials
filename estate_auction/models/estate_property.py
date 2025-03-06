# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    sale_type = fields.Selection(
        [("auction", "Auction"), ("regular", "Regular")], default="regular")
    auction_stages = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("sold", "Sold")], default="draft")
    is_auction_started = fields.Boolean(
        string="Is Auction Started", default=False)
    auction_end_time = fields.Datetime(
        string="End Time", default=datetime.now())
    invoice_id = fields.Many2one(
        "account.move", string="Invoice", readonly=True)
    highest_bidder = fields.Char(
        string="Highest Bidder", readonly=True, store=True, compute="_calculate_bidder_and_price")
    highest_bid_price = fields.Float(
        string="Highest Bid Price", readonly=True, store=True, compute="_calculate_bidder_and_price")

    @api.constrains('auction_end_time')
    def _check_auction_end_time(self):
        for record in self:
            if not record.auction_end_time or record.auction_end_time < datetime.now():
                raise ValidationError(
                    _("Auction end time cannot be in the past or empty!"))

    @api.onchange("sale_type")
    def _onchange_sale_type(self):
        if self.is_auction_started:
            raise UserError(_("Already an Auction was Started"))

    @api.depends("offer_ids.price")
    def _calculate_bidder_and_price(self):
        for record in self:
            auction_offers = record.offer_ids.filtered(
                lambda o: o.offer_type == "auction")
            highest_auction_offer = max(
                auction_offers, key=lambda x: x.price, default=False)

            if highest_auction_offer:
                record.highest_bid_price = highest_auction_offer.price
                record.highest_bidder = highest_auction_offer.partner_id.name
            else:
                record.highest_bid_price = 0.0
                record.highest_bidder = False

    def action_sold_property(self):
        super().action_sold_property()
        for estate_property in self:
            if estate_property.invoice_id:
                raise UserError(
                    _("An invoice is already created for this property."))

            new_invoice = self.env["account.move"].create({
                "partner_id": estate_property.property_buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": estate_property.name,
                        "quantity": 1,
                        "price_unit": estate_property.selling_price
                    })
                ]
            })
            self.invoice_id = new_invoice.id

    def action_open_modualr_type_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add New Offer'),
            'res_model': 'estate.property.offer.wizard',
            'views': [[False, 'form']],
            'target': 'new',
        }

    def action_start_auction(self):
        if self.auction_end_time == False:
            raise UserError(
                _("Please Select Appropriate End Time For Auction"))

        self.is_auction_started = True
        self.auction_stages = "active"

    def action_view_invoice(self):
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("No invoice is linked to this property."))

        return {
            "name": "Property Invoice",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": self.invoice_id.id,
            "target": "current",
        }

    def automate_auction(self):
        properties = self.search(
            [('state', 'in', ('new', 'offer_received')), ("sale_type", "=", "auction"), ("is_auction_started", "=", True)])
        for record in properties:
            if record.auction_end_time and datetime.now() > record.auction_end_time:
                best_offer = self.env['estate.property.offer'].search([
                    ('property_id', '=', record.id)
                ], order='price desc', limit=1)

                if best_offer:
                    best_offer.action_accept_offer()
                    record.auction_stages = 'sold'
                    record.is_auction_started = False
                    record.state = "sold"
