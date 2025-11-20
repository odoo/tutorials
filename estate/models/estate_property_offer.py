from odoo import api, fields, models
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = date_utils.add(
                (offer.create_date or fields.Date.today()), days=offer.validity
            )

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (
                offer.date_deadline - (offer.create_date.date() or fields.Date.today())
            ).days
