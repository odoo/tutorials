from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ESTATE property tag"

    currency_id = fields.Many2one(
        "res.currency",
        related="property_id.currency_id")
    price = fields.Monetary(currency_field='currency_id')
    state = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, compute="_compute_validity", inverse="_inverse_validity")
    date_deadline = fields.Date()

    @api.depends("date_deadline", "create_date")
    def _compute_validity(self):
        for record in self:
            start_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )

            if record.date_deadline:
                record.validity = (
                    record.date_deadline - start_date
                ).days
            else:
                record.validity = record.default_get(["validity"])["validity"]
                # would be easier to use a const?

    def _inverse_validity(self):
        for record in self:
            start_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = start_date + relativedelta(days=record.validity)
