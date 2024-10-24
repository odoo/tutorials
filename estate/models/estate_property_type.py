from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property type"

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', "This type name already exists."),
    ]
    _order = "name asc"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Linked Offers")
    offer_count = fields.Integer("Nb. Linked Offer", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
