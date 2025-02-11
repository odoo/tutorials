from odoo import fields, models 

class Estate_Property_Type (models.Model):
    _name = "estate_property_type_model"
    _description = "This is a property type model"

    name = fields.Char(required=True)
    