from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order="sequence"


    name = fields.Char('Property Type', required=True)

    property_ids = fields.One2many('estate.property','property_type_id')

    sequence = fields.Integer('Sequence')
   
    _sql_constraints = [
    ('estate_property_type_name_unique', 'UNIQUE(name)', 'The property type must be unique.')]
    


