from odoo import fields, models


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type'
    _order = "sequence, name desc"
    _rec_name = "id"

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    property_ids = fields.One2many(
        'real.estate',
        'property_type_id',
        string='Properties'
    )
    offer_ids = fields.One2many(
        "real.estate.property.offer",
        "property_type_id",
        string="Offers"
    )
    _unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
