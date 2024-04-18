from odoo import api, fields, models


class PropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property types"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'A property type name must be unique.')
    ]

    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
