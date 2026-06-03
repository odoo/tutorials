from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'type'

    _unique_property_type = models.Constraint(
        'UNIQUE (type)',
        'The Property Type must be Unique',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=1
    )
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )
    type = fields.Char(required=True)
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_see_offers(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('estate.estate_property_offer_action')
        action['domain'] = [('property_type_id', '=', self.id)]
        return action
