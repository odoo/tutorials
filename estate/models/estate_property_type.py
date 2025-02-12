from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="All Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to order Types. Lower is better.")
    offer_count = fields.Integer("Offers", compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "A type with same name is already exists."),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
