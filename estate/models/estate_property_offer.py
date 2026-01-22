from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    _check_price = models.Constraint(
        "CHECK (price > 0)",
        "A property offer price must be strictly positive",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda x: x.status == "accepted"):
                raise UserError("Only one offer can be accepted")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
