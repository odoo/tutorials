from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order the property types. Lower numbers are displayed first.")

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offers_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offers_count = fields.Integer(string="Offers Count", compute="_compute_offers_count")

    _check_property_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property type must be unique.'
    )

    @api.depends("offers_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offers_count = len(record.offers_ids)