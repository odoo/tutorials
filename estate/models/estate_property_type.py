from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of property'
    _order = 'name asc'

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer("Count", compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_name', 'unique(name)', "A property type name must be unique"),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            if record.offer_ids:
                record.offer_count = len(record.offer_ids)
            else:
                record.offer_count = 0
