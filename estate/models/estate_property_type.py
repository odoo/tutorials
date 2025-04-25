from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=1,
        help="Used to order property types. Lower is better.")
    property_ids = fields.One2many("estate.property", "id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "A property type with the same name already exists.",
        )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids) if record.offer_ids else 0
