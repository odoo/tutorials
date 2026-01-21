from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )

    _positive_price = models.Constraint(
        "CHECK (price > 0)",
        "Price must be positive",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(
                base_date,
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                message = "Another offer already accepted"
                raise UserError(message)
            if record.property_id.state == "sold":
                message = "Property is already sold"
                raise UserError(message)
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
