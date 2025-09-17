from odoo import fields, models, api, _


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name asc"

    name = fields.Char(required=True, string="Type")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Offers", compute="_compute_offer_count", store=True
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "A Property Type with the same name exists.",
        )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Offers"),
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("id", "in", self.offer_ids.ids)],
        }
