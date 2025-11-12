# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    sale_type = fields.Selection([
        ('auction', 'Auction'),
        ('regular', 'Regular')
    ], string='Sale Type', default='regular', required=True, tracking=True)
    auction_end_time = fields.Datetime(string='Auction End Time', default=lambda self: fields.Datetime.now() + timedelta(hours=24))
    highest_offer = fields.Float(string='Highest Offer', compute='_compute_highest_offer', store=True, readonly=True, copy=False)
    highest_bidder_id = fields.Many2one('res.partner', string='Highest Bidder', compute='_compute_highest_bidder', store=True, readonly=True, copy=False)
    auction_started = fields.Boolean(string='Auction Started', default=False, readonly=True, copy=False)
    auction_status = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction Started'),
        ('sold', 'Sold')
    ], default='template', copy=False, tracking=True)
    invoice_id = fields.Many2one('account.move', string="Invoice")

    _sql_constraints = [('check_auction_end_time', 'CHECK(auction_end_time > create_date)', 'The auction end time must be in the future.')]

    @api.depends('offer_ids', 'offer_ids.price')
    def _compute_highest_offer(self):
        for prop in self:
            prop.highest_offer = max(prop.offer_ids.mapped('price'), default=0.0)

    @api.depends('offer_ids', 'offer_ids.price', 'offer_ids.partner_id')
    def _compute_highest_bidder(self):
        for prop in self:
            if prop.offer_ids:
                highest_offer = max(prop.offer_ids.mapped('price'))
                highest_offer_record = prop.offer_ids.filtered(lambda o: o.price == highest_offer).sorted('create_date')
                prop.highest_bidder_id = highest_offer_record[0].partner_id if highest_offer_record else False
            else:
                prop.highest_bidder_id = False

    def action_start_auction(self):
        for record in self:
            if record.auction_started:
                raise UserError(_("Auction has already been started."))
            if not record.auction_end_time:
                raise UserError(_("Please set an auction end time before starting."))
        self.write({'auction_started': True, 'auction_status': 'auction'})

    def _cron_check_auction_end(self):
        auctions = self.search([
            ('sale_type', '=', 'auction'),
            ('auction_started', '=', True),
            ('status', 'not in', ['sold', 'cancelled']),
            ('auction_end_time', '<=', fields.Datetime.now())
        ])
        for auction in auctions:
            if auction.highest_bidder_id and auction.highest_offer > 0:
                all_offers = auction.offer_ids.filtered(lambda o: o.status not in ['accepted', 'refused'])
                highest_offer = auction.offer_ids.filtered(
                    lambda o: o.partner_id == auction.highest_bidder_id and
                    o.price == auction.highest_offer and
                    o.status not in ['accepted', 'refused']
                )
                if highest_offer:
                    highest_offer[0].action_accept_offer()
                    auction.write({
                        'status': 'sold',
                        'auction_status': 'sold',
                        'selling_price': auction.highest_offer,
                        'buyer_id': auction.highest_bidder_id.id
                    })
                self._notify_winning_bidder(highest_offer[0])
                other_offers = all_offers - highest_offer
                if other_offers:
                    self._notify_losing_bidders(other_offers)
            else:
                auction.write({
                'status': 'cancelled',
                'auction_status': 'template',
                'auction_started': False
                })
                auction.message_post(body=_("Auction was cancelled due to no valid bids."))

    def _notify_winning_bidder(self, offer):
        if offer.partner_id or offer.partner_id.email:
            mail_values = {
                'subject': f"Congratulations! Your bid for {offer.property_id.name} was accepted",
                'body_html': f"""
                    <div style="margin: 1px; padding: 0px;">
                        <p style="margin: 1px; padding: 0px; font-size: 13px;">
                            Dear {offer.partner_id.name},
                            <br/><br/>
                            Congratulations! Your bid of {offer.price} for the property "{offer.property_id.name}" has been accepted.
                            <br/><br/>
                            Our team will contact you shortly to proceed with the purchase.
                            <br/><br/>
                            Thank you for your participation!
                            <br/><br/>
                            Best regards,
                            <br/>
                            {self.env.company.name}
                        </p>
                    </div>
                """,
                'email_to': offer.partner_id.email,
                'email_from': self.env.company.email or 'noreply@localhost',
                'auto_delete': True,
            }
            self.env['mail.mail'].sudo().create(mail_values).send(raise_exception=False)
        return True

    def _notify_losing_bidders(self, offers):
        for offer in offers:
            if offer.partner_id or offer.partner_id.email:
                mail_values = {
                    'subject': f"Update on your bid for {offer.property_id.name}",
                    'body_html': f"""
                        <div style="margin: 0px; padding: 0px;">
                            <p style="margin: 0px; padding: 0px; font-size: 13px;">
                                Dear {offer.partner_id.name},
                                <br/><br/>
                                Thank you for your participation in the auction for "{offer.property_id.name}".
                                <br/><br/>
                                We regret to inform you that your bid of {offer.price} was not the highest bid at the end of the auction period.
                                <br/><br/>
                                We appreciate your interest and hope you will participate in our future auctions.
                                <br/><br/>
                                Best regards,
                                <br/>
                                {self.env.company.name}
                            </p>
                        </div>
                    """,
                    'email_to': offer.partner_id.email,
                    'email_from': self.env.company.email or 'noreply@localhost',
                    'auto_delete': True,
                }
                self.env['mail.mail'].sudo().create(mail_values).send(raise_exception=False)
        return True

    def action_generate_invoice(self):
        for record in self:
            if record.status != 'sold':
                raise UserError(_("You can only generate an invoice for sold properties."))
            if record.invoice_id:
                raise UserError(_("An invoice has already been generated."))
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                raise UserError(_("No sales journal found!"))
            try:
                invoice = self.env['account.move'].sudo().create({
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    'name' : f'INV/2025/{record.id}',
                    'invoice_date': fields.Date.today(),
                    'journal_id': journal.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': f"Property Sale: {record.name}",
                        'quantity': 1,
                        'price_unit': record.selling_price
                    })]
                })
                record.invoice_id = invoice.id
                return {
                    'name': _('Invoice'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'res_id': invoice.id,
                    'view_mode': 'form',
                    'target': 'current'
                }
            except Exception as e:
                raise UserError(_("Error generating invoice"))
