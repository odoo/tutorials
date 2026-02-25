from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"
    _rec_name = "id"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count",
    )

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique."
    )

    @api.depends("name", "create_date")
    def _compute_display_name(self):
        for record in self:
            if record.create_date:
                record.display_name = f"{record.name} ({record.create_date.date()})"
            else:
                record.display_name = record.name

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
