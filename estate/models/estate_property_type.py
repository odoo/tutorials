from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence"

    name = fields.Char(string='Type', required=True)
    property_ids = fields.One2many('estate.property', 'type_id', 'Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', 'Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    sequence = fields.Integer('Sequence', default=1)

    _uniq_tag = models.Constraint(
        'unique(name)',
        'Type must be unique',
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_type_properties(self):
        return {
            'name': 'Property offers',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.offer_ids.ids)],
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
        }
