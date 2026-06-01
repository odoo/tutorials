from datetime import timedelta

from odoo import models, fields, api

from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    selling_mode = fields.Selection([
            ('regular', 'Regular'),
            ('auction', 'Auction')
        ],
        string="Selling Mode", default='regular', required=True)

    auction_state = fields.Selection([
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('agreement_sent', 'Agreement Sent'),
            ('in_payment', 'In Payment'),
            ('ended', 'Ended'),
            ('sold', 'Sold')
        ],
        string="Auction State", default='draft', readonly=True)
    auction_end = fields.Datetime(string="Auction End Time")
    # highest_offer = fields.Float(string="Highest Offer", compute="_compute_best_price", readonly=True)
    highest_bidder_id = fields.Many2one("res.partner", string="Highest Bidder", compute="_compute_best_price", readonly=True)
    sign_request_id = fields.Many2one("sign.request", string="Sign Request")
    sign_url = fields.Char(string="Sign URL")
    agreement_signed = fields.Boolean(string="Agreement Signed")
    signature_deadline = fields.Datetime(string="Signature Deadline")

    @api.onchange('selling_mode')
    def _onchange_selling_mode(self):
        for record in self:
            if record.selling_mode == 'auction':
                record.auction_state = 'draft'
            else:
                record.auction_state = False

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        super()._compute_best_price()
        for record in self:
            highest_offer = record.offer_ids[:1]
            record.highest_bidder_id = highest_offer.partner_id

    def write(self, vals):
        for record in self:
            if (vals.get('selling_mode') == 'regular' and record.auction_state in ['in_progress', 'sold', 'ended']):
                raise ValidationError("You cannot change selling mode after auction starts.")
        return super().write(vals)

    @api.model
    def _cron_close_auction(self, job_count=20):
        domain = [
            ('selling_mode', '=', 'auction'),
            ('auction_state', '=', 'in_progress'),
            ('auction_end', '<=', fields.Datetime.now())
        ]
        expired_auction_offer = self.search(domain, order='auction_end asc', limit=job_count)

        accepted_template = self.env.ref('estate_auction.email_template_auction_offer_accepted')
        rejected_template = self.env.ref('estate_auction.email_template_auction_offer_rejected')

        for property_record in expired_auction_offer:
            high_offer = property_record.offer_ids[:1]
            if high_offer:
                high_offer.action_accept()
                property_record.action_create_sign_request()
                accepted_template.send_mail(high_offer.id, force_send=True)
                # high_offer.property_id._mark_as_sold()
                # property_record.auction_state = 'sold'
                property_record.auction_state = 'agreement_sent'

                accepted_template.send_mail(high_offer.id, force_send=True)
                rejected_offers = property_record.offer_ids.filtered(lambda offer: offer.id != high_offer.id)
                for offer in rejected_offers:
                    rejected_template.send_mail(offer.id, force_send=True)
            else:
                property_record.auction_state = 'ended'

    def action_start_auction(self):
        for record in self:
            if record.selling_mode != 'auction':
                raise UserError("This property is not auction type.")
            if not record.auction_end:
                raise UserError("Please set auction end time.")
            record.auction_state = 'in_progress'

    def action_end_auction(self):
        accepted_template = self.env.ref('estate_auction.email_template_auction_offer_accepted')
        rejected_template = self.env.ref('estate_auction.email_template_auction_offer_rejected')
        for record in self:
            # if not record.offer_ids:
            #     raise UserError("Atleast add one offer")
            high_offer = record.offer_ids[:1]
            if high_offer:
                high_offer.action_accept()
                # high_offer.property_id._mark_as_sold()
                # record.auction_state = 'sold'
                record.action_create_sign_request()
                accepted_template.send_mail(high_offer.id, force_send=True)
                record.auction_state = 'agreement_sent'

                rejected_offers = record.offer_ids.filtered(lambda offer: offer.id != high_offer.id)
                for offer in rejected_offers:
                    rejected_template.send_mail(offer.id, force_send=True)
            else:
                record.auction_state = 'ended'

    def action_view_website_property(self):
        for record in self:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/properties/{record.id}',
                'target': 'self',
            }

    def action_create_sign_request(self):
        sign_template = self.env['sign.template'].search([('name', '=', 'auction_agreement.pdf')], limit=1)
        if not sign_template:
            raise UserError("Auction Agreement template not found.")
        role = sign_template.sign_item_ids[:1].responsible_id
        base_url = self.get_base_url()
        for record in self:
            if not record.buyer_id:
                raise UserError("Buyer not found.")
            deadline = (fields.Datetime.now() + timedelta(days=2))
            sign_request = self.env['sign.request'].create({
                'template_id': sign_template.id,
                'reference': f'Auction Agreement - {record.name}',
                'subject': 'Property Auction Agreement',
                'message': ('Please sign the auction agreement.'),
                'validity': deadline.date(),
                'request_item_ids': [(0, 0, {'partner_id': record.buyer_id.id, 'role_id': role.id})]
            })
            sign_request_item = sign_request.request_item_ids[:1]
            # sign_url = sign_request_item.access_url
            sign_url = (
                f"{base_url}"
                f"/sign/document/"
                f"{sign_request.id}/"
                f"{sign_request_item.access_token}"
            )
            record.write({
                'sign_request_id': sign_request.id,
                'signature_deadline': deadline,
                'sign_url': sign_url,
            })

    def action_check_signed_agreement(self):
        for record in self:
            if not record.sign_request_id:
                continue
            sign_request_item = record.sign_request_id.request_item_ids[:1]
            if sign_request_item.signing_date:
                if record.state != 'offer_accepted':
                    continue
                record.agreement_signed = True
                record._mark_as_sold()
                record.auction_state = 'in_payment'

    def action_check_invoice_payment(self):
        properties = self.search([('auction_state', '=', 'in_payment')])
        for record in properties:
            invoice = record.invoice_ids[:1]
            if invoice and invoice.payment_state == 'paid':
                record.auction_state = 'sold'
