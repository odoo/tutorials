from odoo import fields, models 

class Estate_Property_Type (models.Model):
    _name = "estate_property_type_model"
    _description = "This is a property type model"

    name = fields.Char(required=True)
    
    # description = fields.Char()
    # postcode = fields.Integer()
    # available_from = fields.Date(copy=False, default=fields.Date.today())
    # expected_price = fields.Float(required=True, copy=False, string="Expexted_Price")
    # selling_price = fields.Float(readonly=True)
    
    