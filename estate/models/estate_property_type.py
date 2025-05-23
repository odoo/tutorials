from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Type for categorizing estate properties'
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'A property type name must be unique!'),
    ]

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    property_ids = fields.One2many('estate.property', 'Property_type_id', 'Properties')

    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids or [])
