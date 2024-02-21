from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True, string="Type")
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _sql_constraints = [
        ('property_type_name_unique', 'UNIQUE (name)', 'The name must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
