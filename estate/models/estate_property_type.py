from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _unique_name = models.Constraint("UNIQUE (name)", "A property type name must be unique")
