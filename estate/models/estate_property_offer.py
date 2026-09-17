from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOfferModel(models.Model):
    _name = "estate_property_offer"
    _description = "An offer for an estate"

    price = fields.Float()
    status = fields.Selection(string='State',
            selection=[
                ('refused', 'Refused'),
                ('accepted', 'Offer Accepted'),
            ],
            copy=False,
        )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate_property", string="Property")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
