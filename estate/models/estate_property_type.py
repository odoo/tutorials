from odoo import fields, models


class propertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Real Estate Properties"
    _order = "name"

    related_property = fields.Integer(compute="_related_property_count")
    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer("Sequence")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property Name")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offer Id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [('name_uniq', "unique(name)", "Name of Property Type must be Unique")]

    def _related_property_count(self):
        for record in self:
            count = self.env['estate.property'].search_count([('property_type_id', '=', record.id)])
            record.related_property = count

    def action_property_list(self):
        related_property_ids = self.env['estate.property'].search([('property_type_id', '=', self.id)]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': ('Property'),
            'res_model': 'estate.property',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_property_ids)],
        }

    def _compute_offer_count(self):
        for record in self:
            count = self.env['estate.property.offer'].search_count([('property_type_id', '=', record.id)])
            record.offer_count = count

    def action_offer_list(self):
        return True
