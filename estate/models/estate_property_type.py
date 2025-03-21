from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate property type'
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count', default=0)

    _sql_constraints = [
        ('unique_property_type', 'unique(name)', 'Property type must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            print(record.offer_ids)
            record.offer_count = len(record.offer_ids)