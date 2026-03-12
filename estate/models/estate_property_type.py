from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type model"
    _order = "sequence,name"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1, help="used to order by sequence")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer("Count", compute="_compute_offer_count")

    _check_name = models.Constraint("unique(name)", "Property type must be unique")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        offers = self.env["estate.property.offer"]._read_group(
            domain=[("property_type_id", "=", self.ids)],
            aggregates=["property_type_id:count"],
        )
        self.offer_count = offers[0][0]
