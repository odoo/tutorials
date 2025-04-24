from odoo import fields, models, api
from odoo.tools import date_utils as du
from datetime import date


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made on a listing"
    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date_actual = (
                date.today() if not record.create_date else record.create_date.date()
            )
            record.date_deadline = du.add(create_date_actual, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date_actual = (
                date.today() if not record.create_date else record.create_date.date()
            )
            record.validity = (record.date_deadline - create_date_actual).days
