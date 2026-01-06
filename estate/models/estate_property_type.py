from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "this is defind the type of properties"

    name = fields.Char("estate_property", required=True)
    _check_unique_type=models.Constraint('UNIQUE(name)',"The Type must be Unique")
