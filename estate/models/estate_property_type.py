from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    # offer_ids = fields.One2many(related="property_ids.property_offer_ids")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_type = models.Constraint(
        'UNIQUE(name)',
        'A property type with that name already exists.'
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
