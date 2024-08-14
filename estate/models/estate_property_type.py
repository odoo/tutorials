from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Which type of property it is i.e apartment, house "
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence")
    _sql_constraints = [("type_uniq", "unique(name)", "Property Type should be unique")]
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
