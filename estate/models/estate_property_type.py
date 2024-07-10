from odoo import fields, models


class Estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    description = fields.Char()
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type"
    )
    related_properties = fields.Integer(compute='compute_related_properties')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='compute_offer_count', default=0)

    def compute_offer_count(self):
        for recored in self:
            recored.offer_count = self.env['estate.property.offer'].search_count([
                ('property_type_id', '=', recored.id)
            ])

    def action_open_related_offers(self):
        related_offer_ids = self.env['estate.property.offer'].search([
            ('property_type_id', '=', self.id),
        ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': ('Properties'),
            'res_model': 'estate.property.offer',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_offer_ids)],
        }

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
