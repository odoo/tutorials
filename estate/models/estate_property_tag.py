from odoo import fields, models


class EstatePropertyTag(models.Model):
    # ------------------
    # Private attributes
    # ------------------

    _name = "estate.property.tag"
    _description = "This class allows to put tags on a property."
    _order = "name"
    _sql_constraints = [
        ('name_tag_constraint', 'UNIQUE(name)',
         'This name tag already exists.')
    ]

    # ------------------
    # Field declarations
    # ------------------

    name = fields.Char(required=True)
    color = fields.Integer()
