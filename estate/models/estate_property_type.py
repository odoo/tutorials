from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    # _rec_name = "bedrooms"
    _order = "sequence"

    name = fields.Char(string="Property Type", required=True)
    bedrooms = fields.Char(string="Bedrooms", required=True)
    sequence = fields.Integer("Sequence", default=10)
    # property_id = fields.Many2one("estate.property", string="Property Id")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="offers",
    )
    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique"
    )

    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends("name", "bedrooms")
    def _compute_display_name(self):
        for record in self:
            if record.bedrooms:
                record.display_name = f"{record.name} ({record.bedrooms})"
            else:
                record.display_name = record.name

    @api.depends("offer_ids", "offer_count")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
