from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Type", required=True)

     # ch-11 ex-3, ex-4
    _order = "sequence, name"

    # chapter-11 exercise-1
    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")

    # ch-11 ex-4
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    # ch-11 ex-12
    offer_ids = fields.One2many("estate.property", "property_type_id")

    offer_count = fields.Integer(compute="_compute_offer_count")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_view_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }