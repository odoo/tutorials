from datetime import timedelta
from odoo import api, models, fields, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        )
    ]
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        string="Deadline",
    )
    create_date = fields.Date(default=fields.Date.today)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True, string="Property Type"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date
                record.validity = delta.days

    def action_accepted(self):
        for record in self:
            if record.property_id.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            ):
                raise exceptions.UserError(
                    "Only one offer can be accepted for a property."
                )
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
            return True

    def action_refused(self):
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "property_id" not in vals:
                raise exceptions.ValidationError(
                    "Property ID is required to create an offer."
                )

            property = self.env["estate.property"].browse(vals["property_id"])

            if property.state in ["offer_accepted", "sold", "cancelled"]:
                raise exceptions.UserError(
                    f"Cannot create an offer. The property is already '{property.state.replace('_', ' ').title()}'."
                )

            if vals["price"] < property.best_offer:
                raise exceptions.ValidationError(
                    f"The offer must be higher than {property.best_offer:.2f}."
                )
            property.state = "offer_received"

        return super(EstatePropertyOffer, self).create(vals_list)
