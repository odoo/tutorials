from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tags'
    _description = "Property tags such as 'cozy','renovated', etc"
    _order = 'name'

    name = fields.Char(required=True,string="")
    color = fields.Integer('Color')
    _sql_constraints  = [
        (
            'unique_property_tag_name',
            'UNIQUE(name)',
            "The name must me unique"
        )
    ]
