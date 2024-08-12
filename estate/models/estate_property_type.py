from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', name='Property Type Id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [('name_uniq', 'unique(name)',
        'A type with the same name already exists')
    ]
