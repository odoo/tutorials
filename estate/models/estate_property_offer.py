from odoo import fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offer Table"

    price = fields.Float("Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.users", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        compute="_date_deadline",
        inverse="_inverse_date_deadline",
        string="Date Deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price >= 0)",
            "The offer price must be strictly positive",
        )
    ]
    _order = "price desc"

    def _date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Date.today() - record.date_deadline).days

    def action_change_offer_state(self):
        param_value = self.env.context.get("param_name", "default_value")

        for record in self:
            if (
                param_value == "accepted"
                and record.property_id.state == "offer accepted"
            ):
                raise UserError("One offer is already accepted for this property.")
            if param_value == "accepted":
                record.status = "accepted"
                record.property_id.state = "offer accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
            elif param_value == "refused":
                if record.status == "accepted":
                    record.property_id.state = "new"
                    record.property_id.buyer_id = None
                    record.property_id.selling_price = 0
                    record.status = "refused"
                else:
                    record.status = "refused"
