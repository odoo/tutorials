from datetime import timedelta

from odoo import api,fields,models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute = "_count_offers_compute",store=True)

    _sql_constraints = [
        ("estate_property_type_constraint","UNIQUE(name)","Each type should be unique" ),
    ]

    @api.depends('offer_ids')
    def _count_offers_compute(self):
        for record in self:
            print(record.offer_ids)
            count = len(record.offer_ids)
            record.offer_count = count
