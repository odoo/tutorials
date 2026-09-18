from odoo import fields, models


class EstatePropertyType(models.Model):
    _name: str = "estate.property.type"
    _description: str | None = None

    name: fields.Char = fields.Char()
    _unique_name = models.Constraint(
        'unique (name)',
        "Type nmust be unique!",
    )
