from odoo import fields, models, Command
from odoo.addons.account.models.account_move import AccountMove


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties'
    _inherit = 'estate.property'

    name = fields.Char('Title', required=True, translate=True)

    def action_btn_sold(self):
        # @SEDI J'ai pas réussi à faire fonctionner avec la plus simple que tu as suggérée. Elle return res.partner(3,) au lieu de res.partner() comme l'autre mais du coup ça marche pas..
        # partner_id = self.salesman_id.partner_id
        partner_id = self.env['estate.property'].browse(self.env.context.get('active_id')).salesman_id.partner_id
        invoicing_price = self.selling_price * 0.06

        values = {
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            "invoice_line_ids": [
                Command.create({
                    "name": "administrative fees",
                    "quantity": "1",
                    "price_unit": 100
                }),
                Command.create({
                    "name": "commission 6%",
                    "quantity": "1",
                    "price_unit": invoicing_price
                })
            ],
        }
        self.env['account.move'].create(values)
        return super().action_btn_sold()
