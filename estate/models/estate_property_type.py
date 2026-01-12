from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "this is property model"
    _order = "name"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _check_unique_propertyType = models.Constraint(
        "UNIQUE(name)", "The Property type must be unique"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )

    offer_count = fields.Integer(
    string="Offer count",
    compute="_compute_offer_count"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
