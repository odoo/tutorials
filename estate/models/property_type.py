from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate_property_type"
    _description = "The type of the property to be sold such as House, apartment, ..."
    _order = "sequence, name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        string="Properties",
        comodel_name="estate_property",
        inverse_name="type_id",
    )
    sequence = fields.Integer(string="Sequence", default=1)

    offer_ids = fields.One2many(
        string="Property type offers",
        comodel_name="estate_property_offer",
        inverse_name="property_type_id",
    )
    offer_count = fields.Integer(string="Offers count", compute="_compute_offers_count")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type names must be unique!",
    )

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
