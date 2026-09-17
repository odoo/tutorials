from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, default="Unknown")
    offers = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type', string="Offers")
    offers_count = fields.Integer(string='Offers count', compute='_compute_offers_count')
    properties = fields.One2many(comodel_name='estate.property', inverse_name='property_type', string='Properties')
    sequence = fields.Integer(string='Sequence', default=1, help='Used to order stages. Lower is better.')

    _unique_type_name = models.Constraint(
        'unique (name)',
        'The name of a property type should be unique.',
    )

    @api.depends('offers')
    def _compute_offers_count(self):
        for record in self:
            record.offers_count = len(record.offers)
