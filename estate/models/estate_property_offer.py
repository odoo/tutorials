from datetime import datetime, timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Estate Property Offer'

    price = fields.Float(
        string='Price',
    )
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate_property',
        string='Property',
        required=True,
    )
    validity = fields.Integer(
        string='Validity',
        default=7,
    )
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
