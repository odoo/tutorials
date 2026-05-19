from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    estate_property_id = fields.Many2one(
        comodel_name="estate.property",
        ondelete="cascade",
        required=True,
    )

    property_type_id = fields.Many2one(related="estate_property_id.estate_property_type_id", store=True)

    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        ondelete="cascade",
        default=lambda self: self.env.user.partner_id.id,
        required=True,
    )

    price = fields.Float(
        string="Price",
        required=True,
        aggregator="max",
    )

    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("refused", "Refused"),
            ("accepted", "Accepted"),
        ],
        default="new", copy=False,
    )

    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_positive_offer = models.Constraint(
        definition="CHECK(price > 0)",
        message="Offer price must be greater than 0",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for estate in self:
            estate.date_deadline = (estate.create_date or fields.Date.today()) + timedelta(days=estate.validity)

    def _inverse_date_deadline(self):
        for estate in self:
            new_validity = (estate.date_deadline - fields.Date.today()).days
            if new_validity < 0:
                raise UserError(self.env._("Validity cannot be negative."))
            estate.validity = (estate.date_deadline - fields.Date.today()).days

    @api.model
    def create(self, vals):
        for new_offer in vals:
            estate_property = self.env["estate.property"].browse(new_offer.get("estate_property_id"))
            if estate_property.status == "sold":
                raise UserError(self.env._("Cannot bid on a sold property"))

            current_lowest_offer = self.env["estate.property.offer"].search(
                domain=[('estate_property_id', '=', new_offer.get("estate_property_id"))],
                order="price asc", limit=1,
            )

            if not current_lowest_offer:
                if estate_property.status == "new":
                    estate_property.set_offer_received()
                return super().create(vals)

            if new_offer.get("price") < current_lowest_offer.price:
                raise UserError(self.env._("Price cannot be lower than current lowest offer"))

            if estate_property.status == "new":
                estate_property.set_offer_received()

        return super().create(vals)

    @api.model
    def write(self, vals):
        updated_price = vals.get("price")
        if not updated_price:
            return super().write(vals)

        current_property_offers_price_asc = self.estate_property_id.estate_property_offer_ids.sorted("price asc")

        if self == current_property_offers_price_asc[0]:
            return super().write(vals)

        if updated_price < current_property_offers_price_asc[0].price:
            raise UserError(self.env._("Price cannot be lower than current lowest offer"))

        return super().write(vals)

    def action_accept_offer(self):
        self.ensure_one()
        for offer in self:
            if fields.Date.today() > offer.date_deadline:
                raise UserError(self.env._("Offer is expired"))

            estate = offer.estate_property_id
            for recur_offer in estate.estate_property_offer_ids:
                if recur_offer.status == "accepted":    # Guard against multiple accepted offers, independent of property status.
                    raise UserError(self.env._("Another offer is already accepted"))

            estate.buyer_id = offer.buyer_id
            estate.selling_price = offer.price
            estate.status = "offer_accepted"

            offer.status = "accepted"
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = "refused"

        estate = self.estate_property_id
        estate.buyer_id = None
        estate.selling_price = None
        estate.status = "offer_received"
        return True
