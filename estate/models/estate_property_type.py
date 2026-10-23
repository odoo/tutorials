from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "estate_property_type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")
    partner_id = fields.Many2one("res.partner")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
