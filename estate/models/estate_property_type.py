from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'the type of the property being sold'
    _order = 'sequence, name'
    sequence = fields.Integer(default = 1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string = 'Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    name = fields.Char(required = True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string = 'Properties')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Property type name must be unique!')
    ]
