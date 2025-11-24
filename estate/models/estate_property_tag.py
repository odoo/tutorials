from odoo import fields, models


class EstatePropertyTag(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index", default=0)

    # ----------------------------------------
    # SQL constraints
    # ----------------------------------------
    _tag_name_unique = models.Constraint("UNIQUE(name)")
