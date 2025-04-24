from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property Type"
    _order = "name"

    name = fields.Char(string="Name")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer("Sequence", default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Number of offers", compute="_compute_offer_count")

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A type must be unique."),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.write({"offer_count": len(record.offer_ids)})
