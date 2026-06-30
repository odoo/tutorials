from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Type", required=True)

    _check_name = models.Constraint("UNIQUE(name)", "Type name must be unique")
