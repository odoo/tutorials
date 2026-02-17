from odoo import models, fields


class PropertyTag(models.Model):

    # -------------------------------------------------------------------------
    # Private attributes
    # -------------------------------------------------------------------------
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    # -------------------------------------------------------------------------
    # Field declarations
    # -------------------------------------------------------------------------
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index")

    # -------------------------------------------------------------------------
    # SQL constraints
    # -------------------------------------------------------------------------
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        "The tag name must be unique."
    )
