from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "All the available offer for the property"
    _order = "price desc"

    property_id = fields.Many2one("estate.property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("refuse", "Refuse"), ("accepted", "Accepted")],
    )
    property_type_id = fields.Many2one(
        "estate.property.types",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        )
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])

            max_offer_price = max(property.offer_ids.mapped("price") or [0])
            if val.get("price", 0) <= max_offer_price:
                raise UserError(
                    "New offer should contain price higher than current one"
                )

            property.state = "offer received"

        return super().create(vals)

    @api.model
    def unlink(self):
        for record in self:
            if record.property_id.state not in ["new", "cancelled"]:
                raise UserError(
                    "You cannot delete a property offer if the property state is not 'New' or 'Cancelled'."
                )
        properties = self.mapped("property_id")
        result = super(EstatePropertyOffer, self).unlink()
        # Check each property and update its state if it has no more offers
        for property in properties:
            if not property.offer_ids:
                property.state = "new"
        return result

    def action_status_accepted(self):
        for record in self:
            if record.status != "refuse":
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
                record.property_id.state = "offer accepted"
                other_offers = record.property_id.offer_ids.filtered(
                    lambda offer: offer.id != record.id
                )
                other_offers.write({"status": "refuse"})

            else:
                raise UserError("One offer is already accepted")
        return True

    def action_status_refused(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.partner_id = False
                record.property_id.selling_price = False
            record.status = "refuse"
        return True
