from odoo import Command, exceptions, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):

        # self.check_access('write')

        if not (self.env.user.has_group('estate.estate_group_user') or self.env.user.has_group('estate.estate_group_manager')):
            raise exceptions.UserError(("Only Property Agent and Manager Can create invoice"))

        for property in self:
            if not property.buyer_id:
                raise exceptions.UserError("Property does not have a customer!")

            partner_id = property.buyer_id.id
            move_type = 'out_invoice'
            invoice_values = {
                'partner_id': partner_id,
                'move_type': move_type,
                'invoice_date': fields.Date.today(),
                "invoice_line_ids": [
                    Command.create({
                        "name" : "Service Fee(6%)",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    Command.create({
                        "name" : "administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ],
            }
            invoice = self.env['account.move'].sudo().create(invoice_values)
            return super().action_sold()
