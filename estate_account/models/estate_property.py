from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):

        # journal = self.env['account.move'].with_context(default_move_type='out_invoice')._search_default_journal()
        # if not journal:
        #     raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        for record in self:
            vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": 1,  # Hardcoding the journal ID for this tutorial, because the default one is MISC for some reason and that's too annoying to fix
                "line_ids": [
                    Command.create({
                        "name": self.env._(f"6% of {record.name} price"),
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06
                    }),
                    Command.create({
                        "name": self.env._(f"Administrative fees"),
                        "quantity": 1,
                        "price_unit": 100.00
                    }),
                ]
            }
            moves = self.env["account.move"].create(vals)

        return super().action_set_sold()
