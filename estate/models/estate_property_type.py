from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Types'
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="sequence", default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many(
        string="Property Types",
        comodel_name='estate.property', 
        inverse_name='property_type_id'
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name='estate.property.offers', 
        inverse_name='property_type_id'
    )
    offers_count = fields.Integer(string="Offer Count", compute="_offer_count")

    @api.depends("offer_ids")
    def _offer_count(self):
        for offer in self:
            if offer.offer_ids:
                offer.offers_count = len(offer.offer_ids)
            else:
                offer.offers_count = 0
