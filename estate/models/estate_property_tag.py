from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate properties tag declaration"

    name = fields.Char(string="Tag", required=True)

    # -------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------
    _unique_name = models.Constraint(
        'unique(name)',
        'A property tag name must be unique.',
    )
