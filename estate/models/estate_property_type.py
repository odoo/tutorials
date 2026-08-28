from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate type model"
    _order = "sequence, name"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "type_id")
    sequence = fields.Integer(default=0)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_type = models.Constraint("UNIQUE(name)", "types should be unique")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type_record in self:
            property_type_record.offer_count = len(property_type_record.offer_ids)
