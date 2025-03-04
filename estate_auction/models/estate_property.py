from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateAccount(models.Model):
    _inherit = "estate.property"

    sale_type = fields.Selection(
        selection=[
            ('regular', 'Regular'),
            ('auction', 'Auction')
        ],
        string="Property Sale Type",
        default='regular',
        required=True
    )
    auction_state = fields.Selection(
        string="Action State",
        help="State of the action",
        selection=[
            ('template', 'Template'),
            ('auction', 'Auction'),
            ('sold', 'Sold'),
        ],
        default='template',
        copy=False,
        tracking=True
    )
    auction_end_time = fields.Datetime(
        string="End Time",
        help="The end time of the auction."
    )
    highest_offer = fields.Monetary(
        string="Highest Offer",
        currency_field='currency_id',
        readonly=True,
        help="The highest offer received in the auction."
    )
    highest_bidder = fields.Char(
        string="Highest Bidder",
        readonly=True,
        help="The highest bidder details in the auction."
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency"
    )
    email_sent = fields.Boolean(
        string="Email Sent",
        help="Indicates if an email has been sent to the highest bidder.",
        default=False
    )

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    @api.onchange('sale_type')
    def _onchange_sale_type(self):
        if self.sale_type != 'auction' and self.offer_ids:
            raise UserError("You cannot change the sale type of a property that has offers.")

        self.auction_state = 'template'

    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------

    def action_start_auction(self):
        for record in self:
            if not record.auction_end_time:
                raise UserError("Please set the end time of the auction.")

            record.auction_state = 'auction'

    def action_sold(self):
        self.auction_state = "sold"
        return super().action_sold()

    # -------------------------------------------------------------------------
    # Cron Job Methods
    # -------------------------------------------------------------------------

    @api.model
    def check_auction_end(self):
        properties = self.search([('sale_type', '=', 'auction'), ('state', 'not in', ['sold', 'canceled'])])
        for property_obj in properties:
            current_time = fields.Datetime.now()
            if not property_obj.auction_end_time:
                continue

            try:
                end_time = fields.Datetime.from_string(property_obj.auction_end_time)
                if not (end_time <= current_time and not property_obj.email_sent):
                    continue

                highest_offer = max(property_obj.offer_ids, key=lambda offer: offer.price, default=None)
                if not highest_offer:
                    property_obj.state = 'canceled'
                    continue

                property_obj.write({
                    'state': 'offer_accepted',
                    'best_price': highest_offer.price,
                    'selling_price': highest_offer.price,
                    'buyer_id': highest_offer.partner_id,
                    'highest_offer': highest_offer.price,
                    'highest_bidder': highest_offer.partner_id.name
                })

                highest_offer.write({'status': 'accepted'})
                accepted_template = self.env.ref('estate_auction.email_template_offer_accepted')
                if accepted_template:
                    property_obj.email_sent = True
                    accepted_template.write({'email_to': highest_offer.partner_id.email})
                    message_id = accepted_template.send_mail(property_obj.id, force_send=True)
                    if message_id:
                        property_obj.message_post(
                            body="Offer accepted, email sent to the highest bidder.", message_type='notification'
                        )

                rejected_offers = property_obj.offer_ids.filtered(lambda offer: offer != highest_offer)
                for low_offers in rejected_offers:
                    low_offers.write({'status': 'refused'})
                    rejected_template = self.env.ref('estate_auction.email_template_offer_declined')
                    if rejected_template:
                        rejected_template.write({'email_to': low_offers.partner_id.email})
                        rejected_template.send_mail(property_obj.id, force_send=True)

            except:
                continue
