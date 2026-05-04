from odoo import api, fields, models


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "A model where property types are defined"
    _order = "sequence, name, id"
    name = fields.Char(required=True, string="Property Type")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id')
    property_ids = fields.One2many(
        'estate.property', inverse_name='property_type_id', string="Properties")
    offer_count = fields.Integer(
        compute='_compute_offer_count')
    sequence = fields.Integer(default=10)

    @api.depends('offer_ids',)
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_redirect_to_offers(self):
        view = 'estate.test_property_offer_action'
        action = self.env['ir.actions.act_window']._for_xml_id(view)
        action['view_mode'] = 'list'
        # action['domain'] = [('property_type_id', 'in', self.id)]
        return action

    _unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'Property type must be unique'
    )
