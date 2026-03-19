from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties",
    )
    sequence = fields.Integer()
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers",
    )
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    _check_name_unique = models.Constraint("UNIQUE(name)", "The type must be unique ")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        self.offer_count = self.env["estate.property.offer"]._read_group(
            domain=[("property_type_id", "=", self.ids)],
            aggregates=["property_type_id:count"],
        )[0][0]
