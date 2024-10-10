from odoo import fields, models # type: ignore

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    
    name = fields.Char(required=True)
    # property_type_id = fields.Integer()