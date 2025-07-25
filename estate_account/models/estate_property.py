from datetime import date, timedelta

from odoo import _, models


class EstateProperty(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _inherit = 'estate.property'

    # ----------------------------------------
    # Action methods
    # ----------------------------------------
    def action_sold_property(self):
        result = super().action_sold_property()

        invoice_vals_list = []
        for property in self:
            if not property.buyer_id:
                raise ValueError(
                    _("Property %(property_name)s has no buyer assigned!", property_name=property.name)
                )

            invoice_val = {
                'name': f"INV/{property.name}",
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_date': date.today(),
                'invoice_date_due': date.today() + timedelta(days=30),
                'invoice_line_ids': [
                    (
                        0,
                        0,
                        {
                            'name': f"{property.name}",
                            'quantity': 1,
                            'price_unit': property.selling_price,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            'name': f"Commission for {property.name}",
                            'quantity': 1,
                            'price_unit': property.selling_price * 0.06,
                        },
                    ),
                ],
            }
            invoice_vals_list.append(invoice_val)

        self.env['account.move'].create(invoice_vals_list)

        return result
