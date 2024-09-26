from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import ValidationError


class estatepropertyoffer(models.Model):
    _name = "estate.property.offer"
    _description = "model for inserting offers"
    _order = "price desc"
    _sql_constraints = [
        (
            "check_offerprice_not_negative",
            "CHECK(price >= 0.0)",
            "The offer price should be greater than 0",
        ),
    ]

    price = fields.Float("price")
    validity = fields.Integer(string="Validity(days)", default=7)
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], string="Status", copy=False
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

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
        for ele in self:
            ele.status = "Accepted"
            ele.property_id.selling_price = ele.property_id.best_price

    def action_reject(self):
        for ele in self:
            ele.status = "Refused"

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.property_id:
            record.property_id.status = "Offer Received"
        if record.price < record.property_id.best_price:
            raise ValidationError("the offer must be higher than best price")
        return record
