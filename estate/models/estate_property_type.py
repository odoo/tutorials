from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ESTATE property type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', "property_type", string="Properties")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', "property_type_id", string='Offers')
    offer_count = fields.Integer(compute='_compute_order_count')

    @api.depends("property_ids.offer_ids")
    def _compute_order_count(self):
        for record in self:
            record.offer_count = len(record.property_ids.mapped("offer_ids"))
