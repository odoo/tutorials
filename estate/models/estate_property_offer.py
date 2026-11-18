# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    _status_options = [
        ('refused', 'Refused'),
        ('accepted', 'Accepted'),
    ]

    price = fields.Float()
    status = fields.Selection(_status_options, copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (Days)")
    deadline = fields.Date(compute='_computed_date_deadline', inverse="_inverted_date_deadline")

    @api.depends('validity', 'create_date')
    def _computed_date_deadline(self):
        for offer in self:
            offer.deadline = fields.Date.add(self._get_start_date(offer), days=offer.validity)

    def _inverted_date_deadline(self):
        for offer in self:
            offer.validity = (offer.deadline - self._get_start_date(offer)).days

    def _get_start_date(self, offer):
            return fields.Date.to_date(offer.create_date) or fields.Date.today()
