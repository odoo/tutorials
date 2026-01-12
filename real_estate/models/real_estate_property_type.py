from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(required=True)

    _check_type_name = models.Constraint('UNIQUE(name)', "Type must be Unique")
