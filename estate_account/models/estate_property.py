from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_button_action(self):
        print("HERE I AM <----------------------------------------------------------------------------")

        move_values = {
            'partner_id' : self.partner_id.id,
            'move_type' : 'out_invoice',
            'invoice_date' : fields.Date.today(),
            'state' : 'draft',
            'invoice_line_ids' : [
                Command.create({
                    "name": "6% of Selling Price",
                    "quantity" : 1,
                    "price_unit" : self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fee",
                    "quantity" : 1,
                    "price_unit" : 100.00,
                })
            ],
            
        }

        invoice = self.env['account.move'].create(move_values)

        print(f"Invoice crated with ID: {invoice.id}")

        return super(EstateProperty, self).sold_button_action()