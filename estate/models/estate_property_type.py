from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of real estate property"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=1)

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Property type already exists!"),
    ]
