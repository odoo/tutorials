from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for real estate properties"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Validity of the offer in days",
    )
    create_date = fields.Datetime(
        default=fields.Datetime.now,
        readonly=True,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
