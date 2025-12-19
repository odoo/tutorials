from odoo import models, fields


class BuildingTag(models.Model):
    _name = "estate.building_tags"
    _description = "Building Tags Model"

    name = fields.Char(required=True)

    _name_uniqueness_constraint = models.Constraint(
        "UNIQUE (name)", "Building tag name must be UNIQUE."
    )
