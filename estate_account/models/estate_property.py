from odoo import Command, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    # === Actions === #
    def action_sold(self):
        for record in self:
            has_access = record.check_access_rights('write', raise_exception=False)
            # print(has_access)
            if not has_access:
                raise UserError("You do not have permission to modify properties.")
            invoice_vals ={
                "name" : "INV/2025/test",
                "partner_id" : record.buyer_id.id,
                "move_type" : "out_invoice",
                "invoice_line_ids" : [
                    Command.create({
                        "name" : record.name, 
                        "quantity" : 1,
                        "price_unit" : record.selling_price * 0.06, 
                    }),
                    Command.create({
                        "name" : "Administrative Fees", 
                        "quantity" : 1,
                        "price_unit" : 100, 
                    }),
                ],
            }
            print(" reached ".center(100, '='))
            invoice = self.env['account.move'].sudo().create(invoice_vals)
        return super().action_sold()
