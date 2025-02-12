from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


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
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store="True",
        string="Property Type",
    )
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
        if self.property_id.state != "offer_accepted":
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.partner_id = self.partner_id
            self.property_id.state = "offer_accepted"
        else:
            raise UserError("You can not accept another offer.")

    def action_refuse(self):
        self.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Validate that the new offer amount is greater than existing offers
            property_id = self.env["estate.property"].browse(vals.get("property_id"))
            if property_id.offer_ids and any(
                offer.price >= vals["price"] for offer in property_id.offer_ids
            ):
                raise UserError(
                    "You cannot create an offer with an amount lower than or equal to an existing offer."
                )

        # Create offers (no need to manually update property state anymore)
        return super(EstatePropertyOffer, self).create(vals_list)

    def write(self, vals):
        if "price" in vals:
            for record in self:
                # Validate that the new offer amount is greater than existing offers
                if record.property_id.offer_ids and any(
                    offer.price >= vals["price"]
                    for offer in record.property_id.offer_ids
                ):
                    raise UserError(
                        "You cannot update an offer with an amount lower than or equal to an existing offer."
                    )
        return super(EstatePropertyOffer, self).write(vals)

