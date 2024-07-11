from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _order = "name"
    _description = "Real_Estate property model"

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)

    related_property = fields.Integer(compute='_compute_related_property')

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def _compute_related_property(self):
        for record in self:
            record.related_property = self.env['estate.property'].search_count([
                ('property_type_id', '=', record.id),
            ])

    def action_related_property(self):
        related_property_ids = self.env['estate.property'].search([
            ('property_type_id', '=', self.id),
        ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': ('property'),
            'res_model': 'estate.property',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_property_ids)],
        }

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
        'A tag with the same name and applicability already exists.')
    ]

    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
