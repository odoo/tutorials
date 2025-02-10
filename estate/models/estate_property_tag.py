from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)

    _sql_constraints = [('name_unique','unique(name)',"this property tag is already exists!")]
