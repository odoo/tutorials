from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model containing property type"
    _order = "name"

    name = fields.Char(required=True, default="Unknown")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(string="offer Count", compute="_compute_offer_count")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    _sql_constraints = [
        (
            "check_unique_type",
            "unique (name)",
            "Type must be unique",
        )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
