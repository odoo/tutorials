from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = "name"

    name = fields.Char(string='Nome', required=True)
    sequence = fields.Integer('Sequence', default=10)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Number of Offers')

    property_ids = fields.One2many(
        "estate.property",  
        "property_type_id",
        string="Properties"
    )   
    
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


class PropertyType(models.Model):
    _name = 'property.type'
    name = fields.Char(string='Type Name')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type name must be unique'),
    ]