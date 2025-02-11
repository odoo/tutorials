from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "These are Estate Module Property Types"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property type name must be unique"),
    ]

    name = fields.Char(string="Name", required=True)
