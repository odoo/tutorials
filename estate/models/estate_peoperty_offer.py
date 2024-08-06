from odoo import fields, models, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string="Offer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline_of_Offer', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # This line will convert "String of date" into date format
                create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                create_date = fields.Date.from_string(offer.create_date)
                if create_date:
                    offer.validity = (fields.Date.from_string(offer.date_deadline) - create_date).days
                else:
                    offer.validity = 7
            else:
                offer.validity = 7
