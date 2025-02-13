# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on property"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must be strictly positive."),
    ]
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store= True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        offers = []
        for val in vals_list:
            property = self.env["estate.property"].browse(val["property_id"])
            if property.state == "sold":
                raise UserError("Cannot create offer for the property which is already sold")
            for offer in property.offer_ids:
                if offer.price > val["price"]:
                    raise UserError(f"The offer must be higher than {offer.price}")
            offer = super().create([val])  
            if offer.property_id.state == "new":
                 offer.property_id.state = "offer_recieved"
            offers.append(offer)
        return offers


    @api.depends("validity")
    def _compute_deadline(self):
        """computes deadline date acc. to the validity days entered"""
        for offer in self:
            if offer.create_date:
                offer.deadline = fields.Date.add(offer.create_date, days=offer.validity)
            else:
                offer.deadline = fields.Date.today()

    def _inverse_deadline(self):
        """computes validity(days) acc. to the deadline date entered"""
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.deadline - offer.create_date.date()).days
            else:
                offer.validity = 7

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError("Offer cannot be accepted on sold property")
            for existing_offer in offer.property_id.offer_ids:
                if existing_offer.status == "accepted":
                    raise UserError("Only one offer can be accepted for a property")
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"

    def action_refuse(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("Accepted offer cannot be refused")
            offer.status = "refused"
