from odoo import api, Command, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = 'estate.property'

    invoice_ids = fields.One2many("account.move", "estate_property_id", string="Invoices")
    invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def action_set_sold(self):
        self.check_access_rights('write')
        self.check_access_rule('write')

        super().action_set_sold()

        for estate in self:
            selling_price = estate.selling_price
            commission = selling_price * 0.06
            # Create the invoice
            # Use sudo() because the user can generate an invoice without the billing access rights.
            self.env['account.move'].sudo().create({
                'name': estate.name,
                'partner_id': estate.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': 1,
                'estate_property_id': estate.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': f"Commission for selling property {estate.name}",
                        'quantity': 1,
                        'price_unit': commission
                    }),
                    Command.create({"name": "Administrative Fees",
                                    "quantity": 1,
                                    "price_unit": 100.0,
                                    }),
                ],
            })
        return True

    def action_view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': "{'move_type': 'out_invoice'}",
            'res_id': self.invoice_ids.id,
        }
