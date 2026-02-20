from odoo import Command, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Adding fields for the estate property model"
    _inherit = ['estate.property']

    def sold_button(self):
        for record in self:
            if not record.buyer_id:
                error_message = "The estate need a buyer to be sold!"
                raise exceptions.UserError(error_message)

            self.env['account.move'].create({
                'invoice_date': fields.Date.context_today(self),
                'move_type': 'out_invoice',
                'partner_id': record.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                    'name': record.name,
                    'quantity': 1.0,
                    'price_unit': record.selling_price,
                    }),
                    Command.create({
                    'name': "I want more money from you",
                    'quantity': 1.0,
                    'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                    'name': "Administrative fees",
                    'quantity': 1.0,
                    'price_unit': 100,
                    }),
                ]})

        return super().sold_button()
