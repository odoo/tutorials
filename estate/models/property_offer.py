from odoo import fields, models
from odoo import api, fields, models
from odoo.tools import date_utils


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_deadline',
        inverse='_inverse_deadline',
    )

    create_date: fields.Datetime  # From Model

    @api.depends('validity')
    def _compute_deadline(self) -> None:
        today = fields.Date.today()

        for record in self:
            create_date = record.create_date or today
            record.date_deadline = date_utils.add(
                create_date,
                days=record.validity,
            )

    def _inverse_deadline(self) -> None:
        for record in self:
            delta_days = (
                record.date_deadline - record.create_date.date()
            ).days if record.date_deadline and record.create_date else 0
            record.validity = delta_days
