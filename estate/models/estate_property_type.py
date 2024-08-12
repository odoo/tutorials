from odoo import api, models, fields


class estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    name = fields.Char(required=True)
    _order = "sequence, name"
    sequence = fields.Integer('Sequence')
    property_list_id = fields.One2many('estate_property', 'property_type')
    offer_ids = fields.One2many("estate_property_offer", "property_type_id", string="offers")
    offer_count = fields.Integer(string="Numbers of offer", compute='_compute_offer_count', store=True)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
