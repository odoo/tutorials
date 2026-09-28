from typing import Required

from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "real estate property offer"

    price = fields.Float()
    status = fields.Selection(selection=
                            [('refused','Refused'),
                            ('accepted', 'Accepted')], copy = False)
    partner_id = fields.Many2one("res.partner", Required=True)
    property_id = fields.Many2one("estate_property", Required=True)
