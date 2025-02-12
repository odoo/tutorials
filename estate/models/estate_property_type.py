from odoo import models, fields, api


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"  # Order by name
    sequence = fields.Integer("Sequence")
    name = fields.Char(string="Name", required=True)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count",store=True)

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The property type name must be unique."),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


