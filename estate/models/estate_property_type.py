from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Table for type of property"
    _order = "sequence"

    name = fields.Char(required=True)
    _check_name = models.Constraint("UNIQUE(name)", "Le nom du type doit être unique")

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Used to order stages. Lower is better.",
    )

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_number_of_offers")

    @api.depends("offer_ids")
    def _number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
