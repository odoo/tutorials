from odoo import fields, models, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = "sequence, name"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    property_offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Estate Property Offers",
        store=True
    )

    property_offer_count = fields.Integer(compute="_compute_offer_count", store=True)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'A property tag name and property type name must be unique.')
    ]

    @api.depends("property_offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.property_offer_count = len(record.property_offer_ids)
