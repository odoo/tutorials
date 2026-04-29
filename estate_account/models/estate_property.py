from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        invoice_vals_list = []

        # Creating invoice values
        for property in self:
            invoice_vals = dict()
            invoice_vals["partner_id"] = self.buyer_id.id

            # Creating invoice lines
            invoice_lines_vals = []
            sold_property_line = Command.create({
                "name": property.name,
                "quantity": 1,
                "price_unit": 0.06 * property.selling_price,
            })
            invoice_lines_vals.append(sold_property_line)

            administrative_fee_line = Command.create({
                "name": "Administrative fees",
                "quantity": 1,
                "price_unit": 100,
            })
            invoice_lines_vals.append(administrative_fee_line)

            invoice_vals["invoice_line_ids"] = invoice_lines_vals
            invoice_vals_list.append(invoice_vals)

        # Creating invoice
        self.env["account.move"].sudo().with_context(default_move_type="out_invoice").create(invoice_vals_list)
        return super().action_sold_property()
