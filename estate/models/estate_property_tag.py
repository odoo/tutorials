from odoo import fields,models


class estate_property_tag(models.Model):
    # Private attributes
    _name = "estate.property.tag"
    _description = "Estate property tag file"
    _order = "name"

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    # Fields declaration
    name = fields.Char('Name',required=True, translate=True, default='Unknown')
    color = fields.Integer("couleur")