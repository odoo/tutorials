from odoo import fields, api, models

class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Types of Properties are stored"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offers", compute="_compute_offer_count")

    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    property_ids = fields.One2many("estate.property", "property_type_id")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [("name", "Unique(name)", "The type should be unique")]
