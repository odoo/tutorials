from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate_classic.property.type"
    _description = "Property type for an estate"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=1)

    property_ids = fields.One2many("estate_classic.property", "property_type_id")
    offer_ids = fields.One2many("estate_classic.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_name", "UNIQUE (name)", "You cannot have two property types with the same name.")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
