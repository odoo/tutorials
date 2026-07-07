from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    sale_mode = fields.Selection([
        ('regular', 'Regular'),
        ('auction', 'Auction'),
        ], default='regular', required=True)
    auction_end_time = fields.Datetime(string="End Time")
    highest_offer = fields.Float(string="Highest Offer", readonly=True)
    highest_bidder_id = fields.Many2one('res.partner', string="Highest Bidder", readonly=True)
    auction_state = fields.Selection([
            ('template', 'Template'),
            ('auction', 'Auction'),
            ('sold', 'Sold'),
        ], default='template', string="Auction State", store=True, tracking=True)
    invoice_ids = fields.One2many('account.move', 'estate_property_id', string="Invoices")
    invoice_count = fields.Integer(compute='_compute_invoice_count')

    def action_start_auction(self):
        self.ensure_one()
        self.auction_state = 'auction'

    @api.model
    def _cron_close_expired_auctions(self):
        properties = self.search([
            ('sale_mode', '=', 'auction'),
            ('auction_state', '=', 'auction'),
            ('auction_end_time', '<=', fields.Datetime.now()),
            ('state', 'not in', ['sold', 'cancelled'])
        ])

        for property in properties:
            winning_offer = property.offer_ids.filtered(lambda o: o.status == 'pending')[:1]

            if not winning_offer:
                continue
            winning_offer.action_accept_offer()

            property.action_send_auction_result_email(winning_offer)
            property.action_send_rejected_offer_email(winning_offer)

            property.write({
                'highest_offer': winning_offer.price,
                'highest_bidder_id': winning_offer.partner_id.id,
                'auction_state': 'sold',
            })

            property.action_sold()

    def action_send_auction_result_email(self, winning_offer):
        self.ensure_one()

        winner_template = self.env.ref('estate_auction.mail_template_auction_winner')
        winner_template.send_mail(winning_offer.id, force_send=True)

    def action_send_rejected_offer_email(self, winning_offer):
        self.ensure_one()

        rejected_template = self.env.ref('estate_auction.mail_template_auction_rejected')
        rejected_offers = self.offer_ids.filtered(
            lambda offer:
                offer.status == 'refused'
                and offer.id != winning_offer.id
        )

        for offer in rejected_offers:
            rejected_template.send_mail(
                offer.id,
                force_send=True
            )

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def action_view_invoices(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': "Invoices",
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('estate_property_id', '=', self.id)]
        }

    def action_sold(self):
        res = super().action_sold()
        invoice = self.env['account.move'].search(
            [
                ('partner_id', '=', self.buyer_id.id),
                ('move_type', '=', 'out_invoice')
            ],
            order='id desc',
            limit=1
        )
        if invoice:
            invoice.estate_property_id = self.id
        return res
