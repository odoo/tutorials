from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties type declaration"

    name = fields.Char(string="Type", required=True)

    # -------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------
    _unique_name = models.Constraint(
        'unique(name)',
        'A property type name must be unique.',
    )
