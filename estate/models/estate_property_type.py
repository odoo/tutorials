from odoo import models, api
from odoo.fields import Char, Integer, One2many


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"
    _order = "sequence, name"

    name = Char(required=True)
    sequence = Integer('Sequence', default=1)

    # relations
    property_ids = One2many("estate.property", "property_type_id")
    offer_ids = One2many("estate.property.offer", "property_type_id")
    offer_count = Integer(default=0, compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
