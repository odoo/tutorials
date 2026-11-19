from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    # region constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property tag name must be unique."
    )
    # endregion
