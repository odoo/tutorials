from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_count = fields.Integer(string="Offers count", compute="_compute_offer")
