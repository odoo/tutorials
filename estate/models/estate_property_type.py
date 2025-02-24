from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order ='sequence, name'

    name = fields.Char(string = 'Property Type',required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string='Offers')
    offer_ids_count = fields.Integer(string='Offer Count',compute='_property_offer_count')
    sequence = fields.Integer(string='Sequence',default=1)

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','Property type must be unique.')
    ]

    def _property_offer_count(self):
        for record in self:
            record.offer_ids_count = len(record.offer_ids)

    def action_property_offers(self):
        view = 'estate.estate_property_offer_action'
        action = self.env['ir.actions.act_window']._for_xml_id(view)
        action['view_mode'] = 'list'
        action['domain'] = [('id', 'in', self.offer_ids.ids)]
        return action
