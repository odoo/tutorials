# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    auction_state = fields.Selection(
        string="Auction Status",
        selection=[
            ("template", "Template"),
            ("blocked", "Auction"),
            ("done", "Sold")
        ]
    )
    selling_mode = fields.Selection(
        string="Selling Mode",
        selection=[
            ("auction", "Auction"),
            ("regular", "Regular")
        ],
        default="regular"
    )
    auction_start_time = fields.Datetime(string="Start Time", copy=False)
    is_auction_ended = fields.Boolean(compute="_compute_auction_ended", copy=False)
    auction_end_time = fields.Datetime(string="End Time")
    auction_highest_offer = fields.Float(string="Highest Offer", compute="_compute_auction_highest_offer")
    auction_highest_bidder = fields.Many2one(
        string="Highest Bidder", comodel_name="res.partner", compute="_compute_auction_highest_offer"
    )

    @api.model
    def auction_check(self):
        domain = [
            ("selling_mode", "=", "auction"),
            ("state", "=", "offer_received"),
            ("auction_state", "=", "blocked"),
            ("auction_end_time", "<=", fields.Datetime.now()),
        ]
        properties = self.search(domain)
        for property in properties:
            highest_offer = self.env["estate.property.offer"]
            for offer in property.offer_ids:
                if offer.price > highest_offer.price:
                    highest_offer = offer
            highest_offer.action_accept_offer()
            property.auction_state = "done"

    def action_start_auction(self):
        if self.selling_mode != "auction":
            raise ValidationError("Please select Autction as selling mode to start auction!")
        if self.auction_start_time:
            raise ValidationError("Auction has already been started")
        if not self.auction_end_time or self.auction_end_time < fields.Datetime.now():
            raise ValidationError("Invalid auction end time!")
        self.update({
            "auction_start_time": fields.Datetime.now(),
            "auction_state": "blocked"
        })
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "info",
                "title": _("Auction Started"),
                "next": {"type": "ir.actions.act_window_close"},
            },
        }

    @api.depends("offer_ids")
    def _compute_auction_highest_offer(self):
        for property in self:
            highest_offer = self.env["estate.property.offer"]
            for offer in property.offer_ids:
                if offer.price > highest_offer.price:
                    highest_offer = offer
            property.auction_highest_offer = highest_offer.price
            property.auction_highest_bidder = highest_offer.partner_id

    def _compute_auction_ended(self):
        for property in self:
            property.is_auction_ended = property.selling_mode == "auction" and fields.Datetime.now() > property.auction_end_time
