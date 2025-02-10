from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(
        "Property Type", required = True,
        help = "This is a Many2One Field that defines the type of a property."
    )

    _sql_constraints = [('type_unique', 'unique(name)', 'Property Type should be unique.')]
