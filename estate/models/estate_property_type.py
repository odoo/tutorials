from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type such as 'house'"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _property_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'Property type names must be unique',
    )
