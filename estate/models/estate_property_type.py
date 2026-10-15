from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this model defines property type"
    _order = "name"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")
    sequence = fields.Integer("Sequence", help="Used to order list.")

    _name_uniq = models.Constraint(
        "unique (name)",
        "A property type name must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
