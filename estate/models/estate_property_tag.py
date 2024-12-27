from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for real state properties"
    _order = "name"


    name = fields.Char(required=True)
    color = fields.Integer(string='Color', default=0)

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Tag names MUST be unique."),
    ]
