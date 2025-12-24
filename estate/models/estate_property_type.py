from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'sequence, name'

    name = fields.Char(
        "Name",
        required=True,
    )
    _name_uniq = models.Constraint(
        'unique(name)',
        'This property type already exists.',
    )
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
    )
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
    )
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
