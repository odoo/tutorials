from dateutil.relativedelta import relativedelta
from odoo import models, api, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _check_price = models.Constraint(
        "CHECK(price > 0)", "Price of an offer must be positive"
    )
    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_date")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(base_date)).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.customer = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0.00
            record.property_id.customer = None
        return True
