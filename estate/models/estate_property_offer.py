from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
    )
    validity = fields.Integer(
        default=7,
        string="Validity (days)"
    )
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string='Deadline',
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date
            if create_date:
                record.date_deadline = (
                        create_date.date() + relativedelta(days=record.validity)
                )
            else:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                        record.date_deadline - record.create_date.date()
                ).days
