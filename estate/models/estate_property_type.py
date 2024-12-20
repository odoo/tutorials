from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types for real state properties"

    name = fields.Char(required=True)
    # property_ids = fields.One2many('estate.property','property_id')

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Type Names MUST be unique."),
    ]
