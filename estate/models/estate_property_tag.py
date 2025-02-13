from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    # -------------------------------------------------------------------------
    # SQL QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'The name of the tag must be unique.')
    ]

    name = fields.Char(
        string="Name",
        help="The name of the property tag.",
        required=True,
    )
    color = fields.Integer(
        string="Color",
        help="The color of the tag."
    )
