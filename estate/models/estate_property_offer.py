from dateutil.relativedelta import relativedelta

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer module'

    name = fields.Char(required=True)
    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )

    validity = fields.Integer(default=7)
    create_date = fields.Date(default=fields.Date.today(), readonly=True)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_compute_inverse_deadline')

    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _compute_inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
        
