# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


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
