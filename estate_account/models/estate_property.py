
from datetime import datetime

from odoo import Command, models
from odoo.exceptions import ValidationError


class EstatePropertyModel(models.Model):
    _inherit = "estate_property"

    def action_sell_property(self):
        accepted_offer = self.offers_ids.search([('status', '=', 'accepted')], limit=1)
        if not accepted_offer:
            raise ValidationError(self.env._("Cannot sell an estate without accepted offer"))
        self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": accepted_offer.partner_id.id,
            "invoice_date": datetime.today(),
            "journal_id": self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id)], limit=1).id,
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1.0,
                    "price_unit": accepted_offer.price * 0.06,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1.0,
                    "price_unit": 100,
                }),
            ],
        })
        return super().action_sell_property()
