from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)

    _check_unique_type_name = models.Constraint('unique(name)',
                                                "You cannot enter a new Property Type with a duplicate name")

    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_offer_counts")

    @api.depends('offer_ids')
    def _offer_counts(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
