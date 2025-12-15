from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name asc'

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=1, help="Use to order property types. Lower is better.",
    )

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_name = models.Constraint(
        "UNIQUE(name)", "A property type name should be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
