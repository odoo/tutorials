from odoo import fields, models


class EstatePropertyTag(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = 'estate.property.tag'
    _description = "Tags for categorizing estate properties."
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE (name)', "Tag name must be unique."),
    ]
    _order = 'name desc'

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    name = fields.Char(required=True)
    color = fields.Integer(help="Color index for the tag")
