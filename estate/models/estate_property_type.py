from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True, default="Unknown")
    offers = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type')
    offers_count = fields.Integer(compute='_compute_offers_count')
    properties = fields.One2many(comodel_name='estate.property', inverse_name='property_type')
    sequence = fields.Integer(default=1, help='Used to order stages. Lower is better.')

    _unique_type_name = models.Constraint(
        'unique (name)',
        'The name of a property type should be unique.',
    )

    @api.depends('offers')
    def _compute_offers_count(self):
        counts = self.env['estate.property.offer']._read_group(
            domain=[('property_type', 'in', self.ids)],
            groupby=['property_type'],
            aggregates=['__count'],
        )
        mapped = {property_type.id: count for property_type, count in counts}
        for record in self:
            record.offers_count = mapped.get(record.id, 0)
