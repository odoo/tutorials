from odoo import models, fields, api
from datetime import timedelta, datetime

class EstatePpropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer description'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )

    # offer Many2one relation with res.partner
    partner_id = fields.Many2one(
        'res.partner',
        required=True
    )

    # offer Many2one realtion with property
    property_id = fields.Many2one(
        'estate.property',
        required=True
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadDeadline", inverse="_inverse_deadDeadline", store=True)

    @api.depends("validity", "create_date")
    def _compute_deadDeadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_deadDeadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days