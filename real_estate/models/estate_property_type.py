from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string="Sequence of property", default=10)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    property_ids = fields.One2many("estate.property", "property_type", string="Properties")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
