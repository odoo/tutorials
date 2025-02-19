from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Types'
    _order = "sequence, name"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(default=1)
    # offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    # offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)",
         "The type name should be unique."),
    ]

    # @api.depends("offer_ids")
    # def _compute_offer_count(self):
    #     for type in self:
    #         type.offer_count = type.offer_ids.count()
