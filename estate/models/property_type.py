from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "property.type"
    _description = "A type of property"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_type_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute="_compute_count")

    @api.depends('offer_ids')
    def _compute_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
