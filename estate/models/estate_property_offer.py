from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is my fourth model"

    # Atomic fieldss

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", 'Accepted'),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Relational fields

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    # Compute methods
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()

            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()

            record.validity = (record.date_deadline - start_date.date()).days
