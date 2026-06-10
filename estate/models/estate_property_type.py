from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate system - Property Type"
    _order = "sequence, name"

    _check_type_name = models.Constraint(
        "UNIQUE(name)",
        'The Property Type name has to be Unique.'
    )

    name = fields.Char(string="Property Type Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer(default=10)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Number of Offers", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
