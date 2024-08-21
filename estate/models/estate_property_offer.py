import logging
from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.ondelete(at_uninstall=False)
    def _check_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = None
            else:
                pass

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            created_date = record.create_date or date.today()
            record.deadline = (
                created_date + timedelta(days=record.validity)
                if record.validity
                else created_date
            )

    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                record.validity = (
                    record.deadline - record.property_id.create_date.date()
                ).days
            else:
                record.validity = 7

    def action_status_accept(self):
        self.status = "accepted"
        price_percent = 0
        if self.property_id.expected_price != 0:
            price_percent = (self.price / self.property_id.expected_price) * 100
        if price_percent > 90:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = "offer_accepted"
            property_id = self.property_id
            try:
                existing_offer = self.search([("property_id", "=", int(property_id))])
                for record in existing_offer:
                    if record.id == self.id:
                        continue
                    else:
                        record.status = "refused"
            except (UserError, ValidationError):
                logging.exception("Error while updating offer status accepted")
        else:
            raise ValidationError("The selling price must be at least 90%")

    def aciton_status_refused(self):
        if self.status == "accepted":
            self.property_id.selling_price = 0
            self.property_id.buyer_id = None
            self.status = "refused"
        else:
            self.status = "refused"

    _sql_constraints = [
        ("check_price", "CHECK(price >= 0)", "The Price of Offer should be positive"),
    ]

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        price = vals.get("price", 0)
        if not property_id:
            raise ValidationError("Property ID is required.")
        property_record = self.env["estate.property"].browse(property_id)
        existing_offers = self.search([("property_id", "=", property_id)])
        max_price = max(existing_offers.mapped("price"), default=0)
        if price < max_price:
            raise UserError("The offer price must be higher than the existing offers.")
        record = super().create(vals)
        if property_record:
            property_record.state = "offer_recived"
        else:
            raise ValidationError("Property record could not be found.")
        return record
