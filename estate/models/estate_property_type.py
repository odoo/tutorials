from odoo import api, fields, models, _


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real-estate property type"
    _order = "sequence, name"

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", _("Property Type already exists."))
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer(default=1)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
