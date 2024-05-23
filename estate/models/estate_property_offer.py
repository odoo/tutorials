from odoo import api, fields, models
from odoo.tools.date_utils import add


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "description"

    price = fields.Float("Price")
    status = fields.Selection(
        copy=False,
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = add(record.create_date, days=record.validity)
            else:
                record.date_deadline = add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days
