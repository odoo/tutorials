from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "name asc"

    property_ids = fields.One2many(
        "estate.property", inverse_name="property_type_id", string="Property"
    )
    name = fields.Char(string="Title", required=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(
        string="Sequence", default=1, help="Used to order types. Lower is better."
    )

    _sql_constraints = [
        (
            "check_unique_name",
            "UNIQUE(name)",
            "Tag already exists.",
        ),
    ]
