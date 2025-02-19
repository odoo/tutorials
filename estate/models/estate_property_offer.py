from odoo import api, fields, models

import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"

    price = fields.Float('Price')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False, required=True)
    property_id = fields.Many2one('estate.property', string='Property', copy=False, required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline Date', compute='_compute_deadline', inverse='_inverse_deadline')
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        default='new',
    )

    def action_set_accepted(self):
        self.write({'state': 'accepted'})

    def action_set_refused(self):
        self.write({'state': 'refused'})

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else fields.Date.today()) + datetime.timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
