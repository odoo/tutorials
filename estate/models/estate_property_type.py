from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [
        ('type_unique', 'UNIQUE (name)', 'Type must be unique')
    ]
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
