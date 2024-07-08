from odoo import fields, models


class propertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Real Estate Properties"
    related_property = fields.Integer(compute="_related_property_count")

    name = fields.Char("Property Type", required=True)
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Name"
    )

    def _related_property_count(self):
        for record in self:
            count = self.env['estate.property'].search_count([('property_type_id', '=', record.id)])
            record.related_property = count

    def action_property_list(self):
        related_property_ids = self.env['estate.property'].search([
            ('property_type_id', '=', self.id),
        ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': ('Property'),
            'res_model': 'estate.property',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_property_ids)],
        }
