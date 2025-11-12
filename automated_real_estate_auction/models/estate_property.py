# -*- coding: utf-8 -*-

from datetime import date, timedelta
from odoo import api, Command, exceptions, fields, models, _


class EstateProperty(models.Model):
    _inherit = "estate.property"

    property_selling_way = fields.Selection(
        default="regular",
        selection=[
            ("auction", "Auction"),
            ("regular", "Regular"),
        ],
        store=True,
        tracking=True
    )

    auction_stages = fields.Selection(
        default="template",
        selection=[
            ("template", "Template"),
            ("auction", "Auction"),
            ("sold", "Sold")
        ],
        tracking=True
    )

    end_time = fields.Datetime(default=lambda self: fields.Datetime.now() + timedelta(hours=24))
    highest_bidder = fields.Many2one("res.partner", compute="_compute_highest_bidder", store=True, copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    auction_started = fields.Boolean()

    def start_auction(self):
        for record in self:
            record.auction_started = True
            record.auction_stages = "auction"

    def invoices_btn(self):
        invoice_name = f'INV/{self.id}'
        invoice = self.env['account.move'].search([('name', '=', invoice_name)], limit=1)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.depends("offer_ids","offer_ids.price")
    def _compute_highest_bidder(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)

    def _cron_check_auction_end(self):
        auctions = self.search([
            ('property_selling_way', '=', 'auction'),
            ('auction_started', '=', True),
            ('status', 'not in', ['sold', 'cancelled']),
            ('end_time', '<=', fields.Datetime.now())
        ])

        for auction in auctions:
            if auction.highest_bidder and auction.best_offer >= auction.expected_price:
                all_offers = auction.offer_ids.filtered(lambda o: o.status not in ['accepted', 'refused'])
                best_offer = auction.offer_ids.filtered(
                    lambda o: o.partner_id == auction.highest_bidder and
                    o.price == auction.best_offer and
                    o.status not in ['accepted', 'refused']
                )
                if best_offer:
                    best_offer[0].action_accept(from_cron=True)  # Pass flag to allow automated acceptance
                    auction.write({
                        'status': 'sold',
                        'auction_stages': 'sold',
                        'selling_price': auction.best_offer,
                        'buyer_id': auction.highest_bidder.id,
                    })

                    self._notify_winning_bidder(best_offer[0])
                    other_offers = all_offers - best_offer
                    if other_offers:
                        self._notify_losing_bidders(other_offers)
                    auction.create_invoice()

            else:
                auction.write({
                    'status': 'cancelled',
                    'auction_stages': 'template',
                    'auction_started': False,
                })

    def create_invoice(self):
        try:
            self.check_access('write')
            invoice = self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'name' : f'INV/{self.id}',
            'invoice_date': date.today(),
            'invoice_line_ids': [
                Command.create({'name': self.name, 'quantity': 1, 'price_unit': self.selling_price}),
                ]
            })
            return invoice
        except:
            raise exceptions.UserError(_("You do not have the necessary permissions to sell this property."))

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
