from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "All property type e.g. House, Manor "
    _order = 'sequence asc,name'

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order stages. Lower is better.")

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')

    offer_count = fields.Integer(compute='_compute_ofer_count', string="Offer Count")

    @api.depends('offer_ids')
    def _compute_ofer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
        return True

    def action_estate_property_offer_view_by_type(self):
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'estate.property.offer',
           'name': self.env._("Offer"),
           'views': [(False, 'list')],
           'domain': [('property_type_id', '=', self.id)],
       }
