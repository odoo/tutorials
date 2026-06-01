from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Types'

    _order = "sequence, name"

    name = fields.Char(string="Type Name", required=True)
    sequence = fields.Integer(default=10)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
