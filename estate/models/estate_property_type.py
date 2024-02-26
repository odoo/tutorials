from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type model"
    _order = "name"


    name = fields.Char(required=True)
    sequence = fields.Integer()

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_count_related_offers")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'Type name should be unique')
    ]

    @api.depends("offer_ids")
    def _count_related_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
