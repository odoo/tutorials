# -*- coding: utf-8 -*-
from odoo import models, exceptions, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):
        values_list = []
        for record in self:
            values_dict = {}
            if not record.buyer_id:
                raise exceptions.UserError(
                    "Cannot prepare account when buyer is not assigned."
                )
            values_dict["partner_id"] = record.buyer_id.id
            values_dict["move_type"] = "out_invoice"
            values_dict["invoice_line_ids"] = [
                Command.create(
                    {
                        "name": f"Commission for {record.name}",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }
                ),
            ]
            values_list.append(values_dict)
        result = super().action_set_state_sold()
        self.env["account.move"].create(values_list)
        return result
