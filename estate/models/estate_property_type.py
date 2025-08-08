# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)',
         'Property type name must be unique.')
    ]
    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property in self:
            property.offer_count = len(property.offer_ids)
