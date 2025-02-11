from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    offer_count = fields.Integer(string="Offers", compute="_compute_offers")

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Type name already exists!"),
    ]

    @api.depends("offer_ids")
    def _compute_offers(self):
        """
        Compute the total number of offers for properties of the given property type.
        """
        for record in self:
            result = self.env["estate.property.offer"]._read_group(
                domain=[("property_id.property_type_id", "=", record.id)],
                groupby=[],
                aggregates=["id:count"],
            )
            record.offer_count = result[0][0] if result else 0
