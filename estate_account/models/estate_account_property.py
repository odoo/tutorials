from odoo import api,fields, models,exceptions, Command
from datetime import date, timedelta

class EstateAccountProperty(models.Model):
    _name = "estate.property"
    _inherit="estate.property"

    def action_sold(self):
        print("overriden correctly")
        move_values = {
        'partner_id' : self.salesperson_id.id,
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
        return super().action_sold()
