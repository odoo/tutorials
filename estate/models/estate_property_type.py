from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(string="Name", required=True)
    property_count = fields.Integer(string='Property count', compute="_compute_property_home_count")

    @api.depends('name')
    def _compute_property_count(self):
        for record in self:
            count = self.env['estate.property'].search_count([('property_type_id', '=', record.id)])
            record.property_count = count

    def action_smart_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'res_model': 'estate.property',
            'view_mode': 'tree,form',
            'domain': [('property_type_id', '=', self.id)],
        }
