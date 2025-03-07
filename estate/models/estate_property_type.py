# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'name'
    _sql_constraints = [
        ('unique_type_name', "UNIQUE(name)", "The property type name must be unique."),
    ]

    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    offer_count = fields.Integer(
        string ="Offer Count", 
        compute="_compute_offer_count"
    )
    property_ids = fields.One2many(
        comodel_name='estate.property', 
        inverse_name='property_type_id', 
        string="Properties"
    )

    property_offer_ids = fields.One2many(
        comodel_name='estate.property.offer', 
        inverse_name='property_type_id', 
        string="Offers"
    )

    @api.depends('property_offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.property_offer_ids.mapped('id'))
