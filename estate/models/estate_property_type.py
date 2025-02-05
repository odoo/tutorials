from odoo import fields, models



class EstatePropertyType(models.Model):
    _name = "property.type"
    _description = "Estate Property Type"



    type_of_property = fields.Char('Property Type', required=True)
   
