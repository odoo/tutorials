from odoo import models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    def action_accept(self):
        res = super().action_accept()
        for record in self:
            if not record.property_id.deal_id:
                deal = self.env["estate.property.deal"].create(
                    {
                        "property_id": record.property_id.id,
                        "name": record.property_id.name,
                        "expected_price": record.property_id.expected_price,
                        "selling_price": record.property_id.selling_price,
                        "buyer_id": record.property_id.buyer_id.id,
                        "salesperson_id": record.property_id.salesperson_id.id,
                        "description": record.property_id.description,
                        "date_availability": record.property_id.date_availability,
                        "state": record.property_id.state,
                    }
                )
                record.property_id.deal_id = deal.id

        return res
