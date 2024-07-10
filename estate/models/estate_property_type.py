from odoo import models, fields


class Testing_type(models.Model):
    _name = "estate.property.type"
    _description = "This is Real Estate property type"

    name = fields.Char("Pro", required=True)
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="property type"
    )
    related_property_count = fields.Integer(compute='_compute_related_property_count')

    def _compute_related_property_count(self):
        for record in self:
            record.related_property_count = self.env['estate.property'].search_count([
                ('property_type_id', '=', record.id)])

    def action_view_properties(self):
        related_property_ids = self.env['estate.property'].search([
            ('property_type_id', '=', self.id),
        ]).ids
        return {
            'name': ('Properties'),
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property',
            'domain': [('id', 'in', related_property_ids)],
            'views': [[False, 'list'], [False, 'form']]
        }

    _sql_constraints = [('check_property_type', 'unique(name)', 'The property type must be unique.')]
