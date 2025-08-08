from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is the model for estate property's tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_unique', 'unique (name)', "Tag name already exists!"),
    ]
