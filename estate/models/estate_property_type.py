from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "What kind of estate property"

    _order = "sequence, name"
    sequence = fields.Integer('Sequence', default=1)

    name = fields.Char('Name', required=True, translate=True)
    offer_count = fields.Integer('Number of Offers', compute='_compute_offer_count')

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _unique_name = models.Constraint('UNIQUE(name)', 'Property type name must be unique.')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
