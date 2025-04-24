from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tag model"
    _order = "name"

    name = fields.Char(required=True)

    # -----------
    # Constraints
    # -----------

    _sql_constraints = [
        ('name_tag_constraint', 'UNIQUE(name)',
         'This name tag already exists.')
    ]
