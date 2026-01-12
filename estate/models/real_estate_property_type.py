from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    name = fields.Char(string="Name")
    property_ids = fields.One2many("real_estate", "property_type_id", required=True)
    sequence = fields.Integer("Sequence")
    offer_id = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique'
    )

    @api.depends("offer_id")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_id)
