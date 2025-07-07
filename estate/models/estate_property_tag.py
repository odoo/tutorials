from odoo import  fields,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property TAG created"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('tag_name_unique','unique(name)','Tag name should be unique')
    ]