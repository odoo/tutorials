from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(
                    offer.create_date,
                    days=offer.validity,
                )
            else:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(),
                    days=offer.validity,
                )

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = int((offer.date_deadline - offer.create_date.date()).days)
            else:
                offer.validity = int((offer.date_deadline - fields.Date.today()).days)

    @api.model_create_multi
    def create(self, vals):
        for offer in vals:
            linked_property = self.env["estate.property"].browse(offer["property_id"])
            if float_compare(offer["price"], linked_property.best_price, 3) == -1:
                msg = "Offer price cannot be lower than an existing offer"
                raise ValidationError(msg)
            linked_property.state = "offer_received"
        return super().create(vals)

    @api.constrains("status", "property_id")
    def _check_south_facing_garden_accept_offer(self):
        for offer in self:
            price_below_expected = float_compare(offer.price, offer.property_id.expected_price, 3) == -1
            if offer.status == "accepted" and offer.property_id.garden_orientation == "south" and price_below_expected:
                msg = "Offers for properties with south facing garden can only be accepted if the price of the offer is above the expected price of the property"
                raise ValidationError(msg)

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
