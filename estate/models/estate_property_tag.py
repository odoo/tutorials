from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A real estate property tag such as cozy, luxurious ..."
    _order = "name"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer()

    # -----------  MODEL CONSTRAINTS  -------------- #

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique'),
    ]
