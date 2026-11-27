from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_name = models.Constraint("UNIQUE(name)", "Type name should be unique.")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_offers(self):
        self.ensure_one()
        return {
            "name": self.env._("Offers"),
            "view_mode": "list,form",
            "res_model": "estate.property.offer",
            "type": "ir.actions.act_window",
            "domain": [("property_type_id", "=", self.id)],
        }
