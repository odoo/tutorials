from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "sequence, name, id"

    name = fields.Char(required=True)

    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    _sql_constraints: list[tuple[str, str, str]] = [
        (
            "unique_name",
            "UNIQUE (name)",
            "Type name should be unique",
        ),
    ]

    property_ids = fields.One2many("estate.property", "property_type_id")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    offer_count = fields.Integer(compute="_compute_offer_count")


    @api.depends("offer_ids")
    def _compute_offer_count(self) -> None:
        record: EstatePropertyType
        for record in self:
            record.offer_count = len(record.offer_ids)
