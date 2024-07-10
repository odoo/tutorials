from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Properties Type defined"

    # sequence manual ordering
    sequence = fields.Integer(string="Sequence", default=1)

    # order
    _order = "name"

    name = fields.Char(string="Name", required=True)
    property_count = fields.Integer(compute="_compute_property_count", string="Property Count")

    # Inline View relation
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    # sql constraints
    _sql_constraints = [('name_unique', 'unique(name)', "Type Name should be unique")]

    # stat button
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    # For stat button to show number of properties related to property type
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

    # For stat button to show number of offers related to property type
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([('property_type_id', '=', record.id)])
