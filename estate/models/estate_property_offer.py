from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property Offers"
    _order = "price desc"

    price = fields.Integer()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, store=True)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    create_date = fields.Date(default=fields.Datetime.today())

    _sql_constraints = [
        ("positive_price", "CHECK(price > 0)", "Expected price cannot be negative.")
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date
            record.validity = delta.days

    def action_confirm(self):
        for record in self:
            self.status = "accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = "offer accepted"
            self.property_id.selling_price = self.price
            return True

    def action_cancel(self):
        for record in self:
            self.status = "refused"
            return True
