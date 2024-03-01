from odoo import fields, models, Command

from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        super().action_set_sold();

        for property_sold in self:
            invoice_vals = {
                'name': f'INV/PROP/{property_sold.id}',
                'move_type': 'out_invoice',
                'partner_id': property_sold.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': property_sold.name,
                        'price_unit': property_sold.selling_price,
                        'quantity': 1
                    }),
                    Command.create({
                        'name': '6% additional cost',
                        'price_unit': property_sold.selling_price * .06,
                        'quantity': 1
                    }),
                    Command.create({
                        'name': 'Administration fees',
                        'price_unit': 100,
                        'quantity': 1
                    })
                ]
            }

            self.check_access_rights('write')
            self.check_access_rule('write')

            # Just for learning purposes
            # if(self.env.user.has_group('estate.estate_group_manager')):
            #     print(" reached ".center(100, '='))
            #     self.env['account.move'].sudo().create(invoice_vals)
            # else:
            #     raise AccessError("You're not allowed to sold this property contact your manager")

            self.env['account.move'].sudo().create(invoice_vals)
