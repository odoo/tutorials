from odoo import models, fields


class BuildingTag(models.Model):
    _name = 'estate.building_tags'
    _description = 'Building Tags'
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_uniqueness_constraint = models.Constraint(
        "UNIQUE (name)", "Building tag name must be UNIQUE."
    )
