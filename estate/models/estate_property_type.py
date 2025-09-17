from odoo import fields, models 


class RealEstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count', string="Offer Count")

    _check_tag_name = models.Constraint(
    'UNIQUE(name)',
    "The type name must be unique.")
 
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
