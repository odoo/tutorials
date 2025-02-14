from odoo import Command, exceptions, fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        # if not self.env.user.has_group('estate_group_manager'):
        #     raise exceptions.AccessError("You do not have permission to sell property.") exercise
        
        res = super().action_sell_property()
        for prop in self:
            prop.check_access('write')
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

            if not journal:
                raise UserError("No sales journal found in the system.")
            invoice_vals = {
                'partner_id': prop.buyer_id.id,
                'move_type': 'out_invoice',  
                'invoice_date': fields.Date.today(),
                'journal_id': journal.id, 
                'invoice_line_ids': [
                    Command.create({
                        "name": prop.name,
                        "quantity": 1,
                        "price_unit": 0.06*prop.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative Cost",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ] 
            }
            self.env['account.move'].create(invoice_vals)
        return res
