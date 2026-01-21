from odoo import api, fields, models
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Estate Property', required=True)
    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_dt = offer.create_date if offer.create_date else fields.Datetime.now()
            offer.date_deadline = (create_dt + timedelta(days=offer.validity)).date()


    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                create_date = offer.create_date.date() if offer.create_date else fields.Datetime.now()
                offer.validity = (offer.date_deadline - create_date).days
