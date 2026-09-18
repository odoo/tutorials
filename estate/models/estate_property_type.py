from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Type", required=True)
    sequence = fields.Integer("Sequence", default=1)

    offer_count = fields.Integer(string="Number of Offers", compute="_compute_offer_count")

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count += len(record.offer_ids)

    def action_open_related_offers(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": ("Offers"),
            "res_model": "estate.property.offer",
            "domain": [("id", "in", self.offer_ids.ids)],
            #"view_type": "list",
            #"view_mode": "list,form",
            "views": [[self.env.ref('estate.estate_property_offer_view_list').id, "list"]],
            "target": "current",
        }
