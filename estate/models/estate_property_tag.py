from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(
        string="Name",
        help="The name of the property tag.",
        required=True,
    )

    # -------------------------------------------------------------------------
    # SQL QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'The name of the tag must be unique.')
    ]
