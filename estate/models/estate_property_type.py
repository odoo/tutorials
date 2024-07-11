from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    sequence = fields.Integer('Sequence', default=1)
    name = fields.Char('Property Type', required=True)
    related_property_count = fields.Integer(compute='_compute_related_property_count')
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offer")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
            ('uniq_property_type', 'unique(name)', 'A Property type name must be unique.'),
        ]

    def _compute_related_property_count(self):
        for record in self:
            record.related_property_count = self.env['estate.property'].search_count([
                ('property_type_id', '=', record.id),
            ])

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

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
