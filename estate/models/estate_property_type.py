from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"
    _sql_constraints = [("unique_type", "UNIQUE(name)", "Type name must be unique")]

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_ids", string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1)
    offers_ids = fields.One2many(
        "estate.property.offers", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(compute="_compute_offers_count")

    @api.depends("offers_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offers_ids)
