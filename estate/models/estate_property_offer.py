from datetime import timedelta

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "offer_price desc"

    offer_price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True, ondelete="cascade"
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(offer_price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            delta = record.date_deadline - create_date.date()
            record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ["sold", "canceled"]:
                raise UserError(
                    "You cannot accept an offer for a sold or cancelled property."
                )
            # if record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
            #     raise UserError("An offer has already been accepted for this property.")
            if record.property_id.state == 'offer_accepted':
                raise UserError("An offer has already been accepted for this property.")

            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.offer_price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, offers):
        # Extract property_id from the first offer
        property_id = offers[0].get("property_id")
        if not property_id:
            raise ValidationError("Property ID is required.")
        # Fetch the related property record
        estate = self.env["estate.property"].browse(property_id)
        if not estate.exists():
            raise ValidationError("The specified property does not exist.")

        if estate.state in ["sold", "canceled"]:
            raise UserError("Cannot create an offer on a sold or canceled property.")
        if estate.state == "offer_accepted":
            raise UserError(
                "Cannot create an offer on a property with an accepted offer."
            )
        curr_max_price = estate.best_price or 0.0
        for offer in offers:
            if curr_max_price >= offer["offer_price"]:
                raise UserError(
                    "The offer price must be higher than the current best price."
                )
            curr_max_price = max(curr_max_price, offer["offer_price"])

        estate.state = "offer_received"
        return super().create(offers)
