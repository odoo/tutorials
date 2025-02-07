from odoo import api,fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This has all the property types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence",default=1,help="Used to order types. Lower the better.")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ("uniq_type", "unique(name)", "Types should have a unique name.")
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        