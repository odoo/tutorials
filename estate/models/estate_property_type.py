from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Real_Estate property model"

    name = fields.Char('Name', required=True)

    related_property = fields.Integer(compute='_compute_related_property')

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
