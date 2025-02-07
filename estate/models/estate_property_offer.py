from datetime import timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    price = fields.Float("Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_confirm(self):
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_refuse(self):
        self.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        # Create offers
        offers = super(EstatePropertyOffer, self).create(vals_list)

        # Update the state of related properties
        offers.mapped("property_id").update_state_based_on_offers()

        return offers

    # Override write method
    def write(self, vals):
        # Update offers
        res = super(EstatePropertyOffer, self).write(vals)

        # Update the state of related properties
        self.mapped("property_id").update_state_based_on_offers()

        return res

    # Override unlink method
    def unlink(self):
        # Store related properties before unlinking
        properties = self.mapped("property_id")

        # Delete offers
        res = super(EstatePropertyOffer, self).unlink()

        # Update the state of related properties
        properties.update_state_based_on_offers()

        return res


