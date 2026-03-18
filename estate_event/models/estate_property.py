from odoo import api, models, fields
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"
    event_id = fields.Many2one("event.event", string="Event")
    contract_ids = fields.One2many("estate.contract", "property_id")

    @api.model
    def create(self, vals):
        property_record = super().create(vals)
        event = self.env["event.event"].create(
            {
                "name": f"house-event - {property_record.name}",
            }
        )

        property_record.event_id = event.id
        return property_record

    def action_open_event(self):

        return {
            "type": "ir.actions.act_window",
            "name": "Event",
            "res_model": "event.event",
            "view_mode": "form",
            "res_id": self.event_id.id,
            "target": "current",
        }

    def action_accept(self):
        res = super().action_accept()

        for offer in self:
            existing_contract = self.env["estate.contract"].search(
                [("offer_id", "=", offer.id)]
            )

            if existing_contract:
                continue

            self.env["estate.contract"].create(
                {
                    "property_id": offer.property_id.id,
                    "offer_id": offer.id,
                    "buyer_id": offer.property_id.buyer_id.id,
                    "salesperson_id": offer.property_id.user_id.id,
                    "state": "scheduled",
                }
            )

        return res

    def action_open_contract(self):
        for record in self:
            return {
                "type": "ir.actions.act_window",
                "res_model": "estate.contract",
                "view_mode": "form",
                "target": "current",
                "context": {
                    "default_property_id": self.id,
                    "default_buyer_id": self.buyer_id.id,
                    "default_price": self.selling_price,
                    "default_salesperson_id": self.user_id,
                },
            }
