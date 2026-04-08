from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence, name"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    _unique_type_name = models.Constraint(
        'unique(name)',
        'The property type name must be unique.'
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
