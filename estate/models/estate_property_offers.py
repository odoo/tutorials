from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Real Estate Property offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Price cannot be less than 0"),
    ]

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property")
    date_deadline = fields.Date(
        default=(datetime.now() + timedelta(days=7)).date(),
        compute="_compute_date_by_validity",
        inverse="_compute_validity_by_date",
        store=True,
    )
    validity = fields.Integer(
        default=7,
        inverse="_compute_date_by_validity",
        compute="_compute_validity_by_date",
        store=True,
    )
    property_state = fields.Selection(
        related="property_id.state", string="Property State"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True, depends=["property_id"]
    )

    @api.depends("date_deadline")
    def _compute_validity_by_date(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (record.date_deadline - datetime.today().date()).days

    @api.depends("validity")
    def _compute_date_by_validity(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = (
                    record.create_date + timedelta(days=record.validity)
                ).date()
            else:
                record.date_deadline = (
                    datetime.today() + timedelta(days=record.validity)
                ).date()

    def action_confirm(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

    def action_cancel(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        if not isinstance(vals, dict):
            raise ValidationError("Unexpected input to create method.")

        property_id = vals.get("property_id")
        if property_id:
            property = self.env["estate.property"].browse(property_id)
            max_price = max(property.offer_ids.mapped("price"), default=0)
            if vals["price"] <= max_price:
                raise ValidationError(
                    f"The offer price should be greater than the current maximum offer price ({max_price})."
                )

        return super(EstatePropertyOffer, self).create(vals)
