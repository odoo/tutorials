from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'It allows to create a new property offer'

    price = fields.Float(required=True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date')
    create_date = fields.Date(default=fields.Date.today(), required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    property_id = fields.Many2one('estate.property', string='Property')
    status= fields.Selection(
        string='State',
        selection=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        default='pending',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today()  + relativedelta(days=record.validity)


    def _inverse_date(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
