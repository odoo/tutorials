from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)", "Property type name must be unqie")
    ]
    _order = "sequence, name"

    name = fields.Char('name', required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)
