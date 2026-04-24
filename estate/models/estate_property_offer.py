from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        help="Status of the offer"
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            days_to_add = record.validity or 0
            record.date_deadline = base_date + relativedelta(days=days_to_add)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()

            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days
            else:
                record.validity = 0

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "the offer price must be strictly positive.",
    )
