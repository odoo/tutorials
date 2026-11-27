from odoo import api, fields, models
from odoo import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_ids = fields.One2many("account.move", "estate_property_id")
    invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def action_do_sell(self):
        for prop in self:
            self.env["account.move"].create({
                "partner_id": prop.buyer_id.id,
                "move_type": "out_invoice",
                "estate_property_id": prop.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": prop.name,
                        "quantity": 1,
                        "price_unit": 0.06 * prop.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            })
        return super().action_do_sell()

    def action_open_invoices(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Invoices",
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("estate_property_id", "=", self.id)],
        }
