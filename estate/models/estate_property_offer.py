from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers for Real Estate App"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "Offer Price for the property should be strictly positive",
        )
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date.date() if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - create_date).days

    @api.model
    def create(self, vals):
        property = self.env["estate.property"].browse(vals.get("property_id"))
        if property.offer_ids:
            if vals.get("price") < property.best_offer:
                raise ValidationError("The offer price should be more than best offer")
        property.status = "offer_receive"
        return super().create(vals)

    def estate_property_offer_action_accept(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Offer is already accepted")
            else:
                # accept the selected offer
                record.status = "accepted"
                record.property_id.write(
                    {
                        "status": "offer_accept",
                        "buyer_id": record.partner_id,
                        "selling_price": record.price,
                    }
                )
                # reject the other offers for same property
                other_offers = record.property_id.offer_ids.filtered(
                    lambda o: o.id != record.id
                )
                other_offers.write({"status": "refused"})

    def estate_property_offer_action_refuse(self):
        for record in self:
            if record.status == "refused":
                raise UserError("Offer is already refused")
            else:
                # refuse the selected offer
                record.status = "refused"
                record.property_id.write({"buyer_id": False, "selling_price": False})
