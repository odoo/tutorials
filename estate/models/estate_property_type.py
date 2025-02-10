from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id',string="Properties")

    _sql_constraints = [('name_unique','unique(name)',"this property type is already exists!")]