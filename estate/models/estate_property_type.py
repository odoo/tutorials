from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order properties. Lower is better."
    )

    # region relationships
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    # endregion

    # region constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique"
    )
    # endregion
