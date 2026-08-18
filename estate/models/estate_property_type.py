from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate type model"

    name = fields.Char()

    _check_unique_type = models.Constraint("UNIQUE(name)", "types should be unique")
