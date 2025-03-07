from odoo import models, fields # type: ignore

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Tags", required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name should be unique.')
    ]
