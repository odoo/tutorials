from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    property_offer_count = fields.Integer(compute="_compute_offer_count", readonly=True)
    sequence = fields.Integer("Sequence", default=1, help="Used to order property_types, depending on their name.")

    _sql_constraints = [("check_property_type_name", "UNIQUE(name)", "Two property types cannot have the same name.")]

    @api.depends("property_offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.property_offer_count = len(record.property_offer_ids)
