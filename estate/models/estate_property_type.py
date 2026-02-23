from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "name"

    name = fields.Char(string="Property Types", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Property"
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    _name_uniq = models.Constraint(
        "unique(name)",
        "A Property Type with the same name already exists.",
    )
