from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Property Tag", required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)',
         'Tags should have unique names.'),
    ]
