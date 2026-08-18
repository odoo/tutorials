from datetime import date, timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection(
        string='Status',
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string='Property',
        required=True,
    )
    validity = fields.Integer(
        string='Validity (days)',
        default=7,
        required=True,
    )
    # Computed Field
    date_deadline = fields.Date(
        string='Date of Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = self._get_date_or_today(record.create_date) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date_or_today = self._get_date_or_today(record.create_date)
            record.validity = (record.date_deadline - create_date_or_today).days

    @staticmethod
    def _get_date_or_today(datetime_to_evaluate):
        """ Returns the date part of a given datetime if present, otherwise returns today's date """
        return datetime_to_evaluate.date() if datetime_to_evaluate else date.today()
