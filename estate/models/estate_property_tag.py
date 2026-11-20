from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "ESTATE property tag"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer(default=0)

    _name_unique = models.UniqueIndex(
        "(LOWER(name))",
        "Tag's name must be unique! Choose another one."
    )
