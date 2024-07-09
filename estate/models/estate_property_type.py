from odoo import fields, models


class Estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    description = fields.Char()
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type"
    )
    related_properties = fields.Integer(compute='compute_related_properties')

    def compute_related_properties(self):
        for recored in self:
            recored.related_properties = self.env['estate.property'].search_count([
                ('property_type_id', '=', recored.id)
            ])

    def action_open_related_properties(self):
        related_properties_ids = self.env['estate.property'].search([
            ('property_type_id', '=', self.id),
        ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': ('Properties'),
            'res_model': 'estate.property',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_properties_ids)],
        }
