from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    validity = fields.Integer(default=7, string="Validity(days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (
                (record.date_deadline - date).days if record.date_deadline else 0
            )
