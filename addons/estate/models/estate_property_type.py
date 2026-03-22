from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name, id"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=1, help="Sequence number")

    _check_name = models.Constraint("UNIQUE(name)", "Name must be unique.")

    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count", compute="_compute_offer_count"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Property Type Line"

    model_id = fields.Many2one("estate.property.type")
    name = fields.Char()
    expected_price = fields.Char()
    state = fields.Char()
