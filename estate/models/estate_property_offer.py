import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate/Property/Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ("check_offer_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive")
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + datetime.timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_confirm(self):
        for offer in self:
            if offer.property_id.state not in ("offer_accepted", "sold"):
                offer.status = "accepted"
                offer.property_id.state = "offer_accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.buyer_id = offer.partner_id

                for other_offer in offer.property_id.offer_ids:
                    if other_offer.id != offer.id:
                        other_offer.status = "refused"
        return True

    def action_refuse(self):
        for offer in self:
            if offer.property_id.state != "offer_accepted" and offer.property_id.state != "sold":
                offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            offer_property = self.env["estate.property"].browse(vals["property_id"])

            if offer_property.state == "new":
                offer_property.state = "offer_received"

            if vals["price"] <= offer_property.best_price:
                raise UserError("The offer must be greater than the other ones")
            
            if offer_property.state == "sold":
                raise UserError("Cannot create offer to a sold property")

        return super().create(vals_list)

    # The other way of doing it
    # @api.model
    # def create(self, vals):
    #    offers = super().create(vals)

    #    for offer in offers:
    #        offer.property_id.state = "offer_received"

    #        if offer.price <= max(offer.property_id.offer_ids.filtered(lambda x: x.id != offer.id).mapped("price"), default=0):
    #            raise UserError("The offer must be greater than the other ones")

    #    return offers
