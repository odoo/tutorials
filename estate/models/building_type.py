from odoo import models, fields


class BuildingType(models.Model):
    _name = "estate.building_type"
    _description = "Building Type"

    name = fields.Char(required=True)

    _name_uniqueness_constraint = models.Constraint(
        "UNIQUE (name)", "Building type name must be UNIQUE."
    )
