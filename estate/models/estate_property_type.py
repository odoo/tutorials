from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'A type name must be unique.',
    )
