from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = 'sequence, name'

    name = fields.Char('Name', required=True)
    related_properties = fields.Integer(compute='_compute_related_properties')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)', 'Type Name must be unique.'),
    ]

    def _compute_related_properties(self):
        for recored in self:
            recored.related_properties = self.env['estate.property'].search_count([
                ('property_type_id', '=', recored.id)
            ])

    def action_open_related_properties(self):
        return {
            'type': 'ir.actions.act_window',
            'name': ('Properties'),
            'res_model': 'estate.property',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('property_type_id', '=', self.id)],
        }

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
