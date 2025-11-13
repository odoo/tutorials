from dateutil.relativedelta import relativedelta

from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

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
            default_creation_date = record.create_date or fields.Date.today()
            record.date_deadline = (
                relativedelta(days=record.validity) + default_creation_date
            )

    def _inverse_date(self):
        for record in self:
            default_creation_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(default_creation_date)
            ).days
