from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = "Estate property type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate_property_offer', 'property_type_id')
    offer_count = fields.Integer("Offers", compute='_compute_offers_count')

    _name_unique = models.Constraint('unique(name)', "Property type name already exists.")

    @api.depends('offer_ids')
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # def action_view_offers(self):
    #     res = self.env.ref("estate.estate_property_offer_action").read()[0]
    #     res["domain"] = [("id", "in", self.offer_ids.ids)]
    #     return res
