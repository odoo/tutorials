# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ]
    )
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner", required=True)
    property_id = fields.Many2one(string="Property", comodel_name="estate.property", required=True)
    property_type_id = fields.Many2one(string="Property Type", related="property_id.property_type_id", store=True)

    _sql_constraints = [("check_offer_price", "CHECK(price > 0)", "Offer price must be stictly positive")]

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])
            if property.state == "sold":
                raise UserError("Offers cannot be made for sold property!")
            max_required_price = self.get_max_required_price(property)
            if max_required_price > val["price"]:
                raise UserError(f"The offer must be higher than {max_required_price}")
            if property.state == "new":
                property.state = "offer_received"
        return super().create(vals)

    def get_max_required_price(self, property):
        return max(property.mapped("offer_ids.price"), default=0)

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            base_date = offer.create_date or fields.date.today()
            offer.date_deadline = fields.Date.add(base_date, days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if not offer.create_date:
                offer.validity = (offer.date_deadline - fields.Date.today()).days
                continue
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        if any([offer.status == "accepted" for offer in self.property_id.offer_ids]):
            raise UserError("An offer was already accepted for this property")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        if self.status == "accepted":
            self.property_id.buyer_id = None
            self.property_id.selling_price = 0
        self.status = "refused"
