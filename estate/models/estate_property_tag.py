from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "My Estate Property Tag"

    name = fields.Char(required = True)

    _sql_constraints = [
        ("unique_name", "unique(name)", "Property tag should be unique.")
    ]