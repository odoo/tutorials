from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate is defined"
    _order = "name asc"
    _sql_constraints = [
            ('check_unique_property_type', 'UNIQUE(name)', 'The Property type should be unique')
        ]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = sum(len(property.offer_ids) for property in record.property_ids)
