from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = 'name'

    name = fields.Char('Name', required=True)
    related_properties = fields.Integer(compute='_compute_related_properties')
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string='Properties')
    sequence = fields.Integer('Sequence', default=1)

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
