from odoo import models, fields, api
from datetime import datetime, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Real Estate Property offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate.property")

    date_deadline = fields.Date(
        compute="_compute_date_by_validity", 
        inverse="_compute_validity_by_date"
    )
    validity = fields.Integer(
        default=7,
        inverse="_compute_date_by_validity",
        compute="_compute_validity_by_date",
    )

    @api.depends("date_deadline")
    def _compute_validity_by_date(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - datetime.today().date()).days
            else:
                record.validity = 0

    @api.depends("validity")
    def _compute_date_by_validity(self):
        for record in self:
            if record.validity is not None:
                record.date_deadline = datetime.today().date() + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = False
