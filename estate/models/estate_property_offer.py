import datetime
from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    create_date = fields.Date(default=datetime.date.today())
    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_compute_validity")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            create_date = (
                record.create_date if record.create_date else datetime.date.today()
            )
            record.deadline = create_date + datetime.timedelta(days=record.validity)

    @api.depends("deadline", "create_date")
    def _compute_validity(self):
        for record in self:
            create_date = (
                record.create_date if record.create_date else datetime.date.today()
            )
            record.validity = (record.deadline - create_date).days
