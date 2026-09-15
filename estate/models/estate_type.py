from odoo import api, fields, models


class EstateType(models.Model):
    _name = 'estate.type'
    _description = 'Estate Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many('estate', 'estate_type_id', string='Properties')
    offer_ids = fields.One2many('estate.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property type name must be unique.",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
