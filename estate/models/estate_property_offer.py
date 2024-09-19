import datetime

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers to estate properties"

    price = fields.Float("Price")
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ], "Status", required=False, copy=False)
    property_id = fields.Many2one("estate.property", "Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Date deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date or datetime.date.today()
            timedelta = datetime.timedelta(days=record.validity)
            record.date_deadline = starting_date + timedelta

    def _inverse_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() or datetime.date.today()
            timedelta = record.date_deadline - starting_date
            record.validity = timedelta.days
