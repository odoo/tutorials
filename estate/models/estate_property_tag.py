from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "ESTATE Property Tag"
    _order = "name"

    name = fields.Char('Name', required=True)
    description = fields.Text(string="Description")
    color = fields.Integer(string="Color")

    # SQL constraints
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property property tag name must be unique',
    )
