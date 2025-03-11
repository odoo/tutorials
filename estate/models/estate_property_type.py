from odoo import api, fields, models


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Help to set type for property"
    _order = "sequence, name, id"  # first priority sequence ,then name, id

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string=" ")
    sequence = fields.Integer(default=1, help="Used to order property types manually")
    offer_type_id = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )

    offer_count = fields.Integer(
        string="Offer Count", compute="_compute_offer_count", store=True
    )

    _sql_constraints = [("unique_type_name", "UNIQUE(name)", "Type must be Unique")]

    @api.depends("offer_type_id")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_type_id)
