from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'estate property type'
    _order = "sequence, name"

    name = fields.Char(string='Type', required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('estate_property', 'property_type_id')
    offer_ids = fields.One2many('estate_property_offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _name_uniq = models.Constraint(
        'unique (name)',
        "A property type name must be unique",
    )

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
