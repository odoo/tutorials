from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

#---------------------------------------Basic Fields---------------------------------------#
    name = fields.Char(required=True)

#---------------------------------------Relational Fields----------------------------------#
    property_ids=fields.One2many("estate.property","property_type_id",string="Properties")
    