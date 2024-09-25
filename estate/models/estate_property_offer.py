from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    price = fields.Float("Price")
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], readonly=True
    )
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property")
    property_type_id = fields.Many2one(related="property_id.property_type", store=True)
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    _sql_constraints = [
        (
            "check_offerprice_not_negative",
            "CHECK(price >= 0.0)",
            "The offer price should be greater than 0",
        ),
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for ele in self:
            if not ele.create_date:
                ele.create_date = date.today()
            ele.date_deadline = ele.create_date + timedelta(days=ele.validity)

    def _inverse_deadline(self):
        for ele in self:
            ele.validity = abs((ele.date_deadline - ele.create_date.date()).days)

    def action_confirm(self):
        for record in self:
            record.status = "Accepted"
            record.property_id.selling_price = record.price

    def action_cancel(self):
        for record in self:
            record.status = "Refused"

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.property_id:
            record.property_id.status = "offer received"
        if record.price < record.property_id.best_price:
            raise ValidationError("the offer must be higher than the best price")
        return record
