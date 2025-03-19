from odoo import models, fields


class PropertyType(models.Model):
    _name = "public.property.type"
    _description = "A different types of properties."
    _order = "name"

    name = fields.Char()
    sequence = fields.Integer()
    property_ids = fields.One2many("public.property", "property_type_id")
    _sql_constraints = [
        ("uniq_property_type", "unique(name)", "A property type must be unique.")
    ]
    offer_ids = fields.One2many('public.property.offer' ,'property_type_id')
    offer_count = fields.Integer(compute ="_compute_offers_given_type")
    def action_related_properties(self):
        for record in self:
            print(record.offer_count)
    def _compute_offers_given_type(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
