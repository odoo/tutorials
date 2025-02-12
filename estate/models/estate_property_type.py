from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Property')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string='Count', compute="_count_offer_ids")

    _sql_constraints = [('name_uniq', 'unique(name)', 'The name must be unique')]

    @api.depends('offer_ids')
    def _count_offer_ids(self):
        for record in self:
            pass
            record.offer_count = len(record.offer_ids)
