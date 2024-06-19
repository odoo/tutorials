from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of real estate property"
    _order = "sequence"

    name = fields.Char(required=True, string="Type")
    property_ids = fields.One2many("estate.property", 'property_type_id')
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for offer_type in self:
            offer_type.offer_count = len(offer_type.offer_ids)

    offer_count = fields.Integer(compute=_compute_offer_count)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property types must be unique')
    ]