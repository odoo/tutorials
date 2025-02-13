# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import api,models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Real Estate Property Type'
    _order = "name asc"
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.'),
    ]

    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    property_offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")
    
    @api.depends("property_offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.property_offer_ids.mapped("id"))
