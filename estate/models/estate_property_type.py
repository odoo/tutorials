from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence"

    name = fields.Char('Type Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many("estate.property", "type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count", default=0)

    api.depends("offer_ids")
    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)

    _uniq_name = models.Constraint(
        'UNIQUE(name)',
        'The type name must be unique'
    )
