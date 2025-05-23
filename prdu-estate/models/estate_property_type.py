from odoo import fields, models, api


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "typie, co ty paczysz?"
    _order = "sequence, name"
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer("Sequence", default=1, help="Used when ordering the list manually")
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Type name must be unique")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
