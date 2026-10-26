from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    _order = "sequence"
    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer(default=1)
    _unique_name = models.Constraint(
        "UNIQUE(name)", "Property type names must be unique"
    )
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="sum_offers")

    @api.depends("offer_ids")
    def sum_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
