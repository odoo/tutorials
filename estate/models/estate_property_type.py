from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Properties Type defined"

    name = fields.Char(string="Name", required=True)
    property_count = fields.Integer(compute="_compute_property_count", string="Property Count")

    # sql constraints
    _sql_constraints = [('name_unique', 'unique(name)', "Type Name should be unique")]

    def _compute_property_count(self):
        for record in self:
            record.property_count = self.env['estate.property'].search_count([('property_type_id', '=', record.id)])

    def action_open_properties(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'view_mode': 'tree,form',
            'res_model': 'estate.property',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }
