from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"


    name = fields.Char(required=True)

    _sql_constraints =[
        ('unique_property_tag','unique(name)','The property tag should be unique')
    ]

   

