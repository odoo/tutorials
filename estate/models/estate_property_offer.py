from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    # type_id = fields.Many2one("estate.property.type", string="Property type")
    type_id = fields.Many2one(related="property_id.type_id")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer Price should be bigger than 0"),
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            if any(r == "accepted" for r in record.property_id.offer_ids.mapped("status")):
                raise UserError("Another offer was already accepted")
            record.status = "accepted"
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = "refused"
