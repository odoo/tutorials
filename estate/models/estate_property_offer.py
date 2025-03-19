from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model containing property offers"
    _order = "price desc"

    price = fields.Float()
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )

    @api.depends("validity")
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
                create_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0.0)",
            "Price must be positive",
        ),
    ]

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        if property_id:
            property_record = self.env["estate.property"].browse(property_id)
            existing_offers = property_record.offer_ids
            if existing_offers:
                max_existing_price = max(existing_offers.mapped("price"))
                new_price = vals.get("price", 0.0)
                if new_price < max_existing_price:
                    raise UserError(
                        f"Cannot create an offer with price {new_price} for property '{property_record.name}'. "
                        f"There is an existing offer with a higher price ({max_existing_price})."
                    )
        return super(EstatePropertyOffer, self).create(vals)
