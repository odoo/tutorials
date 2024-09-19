from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    _order = "sequence, name"

    name = fields.Char(required=True)

    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type must be unique!'),
    ]
