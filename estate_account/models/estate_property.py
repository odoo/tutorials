from odoo import models, Command


class EstatePropertyExtension(models.Model):
    _inherit = 'estate.property'

    def sold_property_button(self):
        """ When an invoice linked to a sales order selling registrations is
        paid confirm attendees. Attendees should indeed not be confirmed before
        full payment. """
        # Set the create function parameters
        values = {"partner_id": self.partner_id.id,
                  "move_type": "out_invoice",
                  "line_ids": [
                    Command.create({
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": self.selling_price
                    }),
                    Command.create({
                        "name": r"6% malus for being ugly",
                        "quantity": 1,
                        "price_unit": 0.06 * self.selling_price
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                  ],
                }
        # Create the invoice
        self.env['account.move'].create(values)
        return super().sold_property_button()
