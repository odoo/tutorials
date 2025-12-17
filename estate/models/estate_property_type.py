# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'name'
    _check_unique_name = models.Constraint('UNIQUE(name)', "The type name must be unique.")

    name = fields.Char(required=True, string="Name")
    sequence = fields.Integer(default=1, string="Sequence")
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string="Properties")
    offer_count = fields.Integer(compute='_compute_offer_count', string="Offer Count")

    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = sum(property_type.property_ids.mapped(lambda p: len(p.offer_ids)))
