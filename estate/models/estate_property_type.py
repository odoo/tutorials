from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Define type of properties'
    _sql_constraints = [('name_unique', 'UNIQUE(name)', "A property type name must be unique")]
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
