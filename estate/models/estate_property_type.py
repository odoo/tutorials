from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property test model'
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "type_id")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
