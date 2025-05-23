from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type for categorizing estate properties'
    _order = 'name asc'

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Type name must be unique!'),
    ]

    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', 'Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', 'Offers')
    offer_count = fields.Integer('Offers Count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
