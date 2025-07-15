from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of properties of estate model"
    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.property", "property_type_id")

    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", "Offer For Property Type"
    )

    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer("Sequence", default=1)

    # sql constrains :::

    _sql_constraints = [
        ("check_uniquness", " UNIQUE(name)", "Type of property name must be unique")
    ]

    # order on which data will be fetched

    _order = "sequence, name desc"

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for data in self:
            data.offer_count = len(data.offer_ids)
