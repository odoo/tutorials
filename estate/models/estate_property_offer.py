from odoo import api, fields, models
from odoo.tools.date_utils import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    date_deadline = fields.Date('Deadline')
    validity = fields.Integer('Validity (days)', default=7, compute='_compute_validity', inverse='_inverse_validity')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    active = fields.Boolean('Active', default=True)

    @api.depends('date_deadline')
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.date.today()).days

    def _inverse_validity(self):
        for record in self:
            if isinstance(record.validity, int):
                record.date_deadline = fields.date.today() + relativedelta(days=record.validity)
