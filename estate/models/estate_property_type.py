from odoo import models, fields, api

class EstatePropertyType(models.Model):

    _name = "estate.property.types"
    _description = "Different kind of estate properties"
    _order = "name"

    name = fields.Char(name = "Type of Estate Property", required = True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate.property", "type_id", name = "Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", name="Offers")
    offer_number = fields.Integer(compute="_count_offers", name =" Offers")

    @api.depends("offer_ids")
    def _count_offers(self):
        for record in self:
            record.offer_number = len(record.offer_ids)
