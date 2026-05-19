from odoo import _, api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property type"
    _order = 'name'

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', store=True)
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('property_ids', 'offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

    @api.readonly
    def action_view_offers(self):
        return {
            'name': _("Offer(s)"),
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'target': 'current',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.property_ids.ids)],
        }
