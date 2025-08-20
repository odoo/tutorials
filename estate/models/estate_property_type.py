from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the type of an estate"
    _order = "sequence,name desc"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_count_offer")

    _sql_constraints = [("unique_property_type", "UNIQUE(name)", "Type name must be unique !")]

    @api.depends("offer_ids")
    def _count_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
