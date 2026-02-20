from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Group properties by type of building"
    _check_name = models.Constraint('UNIQUE(name)', 'This property type already exists')
    _order = "sequence,name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', help="Used to order property types.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offers_count")

    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return True
