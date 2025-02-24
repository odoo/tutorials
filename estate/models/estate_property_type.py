# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api
from odoo import fields
from odoo import models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = 'sequence, name'
    _sql_constraints = [
        ('property_type_unique', "UNIQUE(name)",
        "Type with same name already exists"),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for propertytypes in self:
            propertytypes.offer_count=len(propertytypes.offer_ids)
