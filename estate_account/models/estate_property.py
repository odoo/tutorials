from odoo import Command, models
from odoo.fields import Date


class InheritedEstatepropertyModel(models.Model):
    _inherit = 'estate.property'

    def action_set_property_sold(self):
        self.env['account.move'].check_access('create')
        self.env['account.move'].create(
            vals_list={
                'name': f"INV/Property/{self.name}",
                'invoice_origin': self.name,
                'partner_id': self.buyer_id.id,
                'invoice_date': Date.today(),
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': f"commision for {self.name}",
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06
                    }),
                    Command.create({
                        'name': 'Administration Fee',
                        'quantity': 1,
                        'price_unit': 100.0
                    })
                ]
            }
        )
        return super().action_set_property_sold()
