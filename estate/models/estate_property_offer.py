from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        "estate.property", required=True, ondelete="cascade"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_validity = models.Constraint(
        "CHECK(validity >= 0)", "Validity days cannot be negative!"
    )
    _check_price = models.Constraint(
        "CHECK(price > 0)", "An offer price must be strictly positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = start_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                start_date = (
                    offer.create_date.date()
                    if offer.create_date
                    else fields.Date.today()
                )
                offer.validity = (offer.date_deadline - start_date).days

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        self._inverse_date_deadline()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")
            if property_id and price:
                property_record = self.env["estate.property"].browse(property_id)
                # Check if new price is lower than any existing offer
                if property_record.offer_ids:
                    max_offer = max(property_record.offer_ids.mapped("price"))
                    if price < max_offer:
                        raise UserError(_("The offer must be higher than %s", max_offer))

                # Update property state
                if property_record.state == "new":
                    property_record.state = "offer_received"

        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            if "accepted" in offer.property_id.offer_ids.mapped("status"):
                raise UserError(_("An offer has already been accepted"))
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"

            for other_offer in offer.property_id.offer_ids:
                if other_offer.id != offer.id:
                    other_offer.status = "rejected"

        return True

    def action_reject(self):
        for offer in self:
            offer.status = "rejected"
        return True
