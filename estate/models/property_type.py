from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char("Name")
    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="property_type_id"
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to manually drag and change sequence"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="offers",
    )
    offer_count = fields.Integer(
        string="offer Count", compute="_compute_offer_count", store=True
    )

    _sql_constraints = [
        (
            "property_type_name_unique",
            "UNIQUE(name)",
            "The property type name must be unique.",
        )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
