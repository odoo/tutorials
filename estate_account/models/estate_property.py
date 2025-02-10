from odoo import api, Command, fields, models
from odoo.exceptions import UserError

class estateProperty(models.Model):
    _inherit = "estate.property"

    def set_sold(self):
       for property in self:
           if property.state != "offer_accepted":
               raise UserError("You can only sell properties with an accepted offer.")   
           # Create the account.move (invoice)
           invoice = self.env["account.move"].create({
               "partner_id": property.buyer_id.id,  # Buyer is the partner
               "move_type": "out_invoice",  # Customer Invoice
               "invoice_line_ids": [
                   # Invoice line for 6% of the selling price
                   Command.create({
                       "name": "Selling Commission (6%)",
                       "quantity": 1,
                       "price_unit": property.selling_price * 0.06,
                   }),
                   # Invoice line for the administrative fees (fixed 100.00)
                   Command.create({
                       "name": "Administrative Fees",
                       "quantity": 1,
                       "price_unit": 100.00,
                   }),
               ],
           })   
           # Mark the property as sold
           property.state = "sold"   
       return super().set_sold()
