from odoo import fields, models, Command, api


class EstateAccountProperty(models.Model):
    _inherit = "estate.property"
    move_ids = fields.One2many(comodel_name='account.move', inverse_name='property_id', string='Moves')
    move_count = fields.Integer('Invoice Count', compute='_compute_move_count', default=0)

    @api.depends('move_ids')
    def _compute_move_count(self):
        for record in self:
            record.move_count = len(record.move_ids)

    def _create_account_move(self):
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                self.env['account.move'].create([
                    dict(
                        partner_id=offer.partner_id.id,
                        move_type="out_invoice",
                        line_ids=[
                            Command.create(dict(name="6% Down Payment", quantity=0.06, price_unit=offer.price)),
                            Command.create(dict(name="Administrative Fees", quantity=1, price_unit=100))
                        ],
                        property_id = self.id,
                    )]
                )
                return


    def action_property_sold(self):
        for property in self:
            property._create_account_move()

        return super().action_property_sold()
