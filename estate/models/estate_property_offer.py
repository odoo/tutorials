from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Monetary(currency_field="currency_id")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        help="Status of the offer"
    )
    validity = fields.Integer(default=7, string="Validity (days)")

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "the offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()

            delta = record.date_deadline - base_date
            record.validity = delta.days

    @api.model
    def create(self, vals):

        offer = super().create(vals)
        offer.property_id.state = "offer_received"

        return offer

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        self.status = "refused"
        return True
