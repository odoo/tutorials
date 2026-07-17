from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "model for estate property types"
    _order = "name"

    name = fields.Char(required=True)
    _name_uniq = models.Constraint(
        "unique(name)",
        "A type with the same name already exists in property type.",
    )
    sequence = fields.Integer("Sequence")
    property_ids = fields.One2many(
        "estate.property",
        "property_type",
        string="Properties",
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string="offers",
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count",
    )

    @api.depends("property_ids.offer_ids")
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = self.env['estate.property.offer'].search_count(
                [
                    ('property_type_id', '=', prop_type.id),
                ],
            )
