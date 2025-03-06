# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyAuction(models.Model):
    _inherit = 'estate.property'

    sale_type = fields.Selection([
        ('regular', 'Regular'),
        ('auction', 'Auction')
    ], string="Sale Type", required=True, default='regular')

    auction_end_time = fields.Datetime(string="Auction End Time", required=False)
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    highest_offer = fields.Monetary(
        string="Highest Offer", readonly=True, currency_field="currency_id")
    highest_bidder = fields.Many2one(
        "res.partner", string="Highest Bidder", readonly=True)

    is_auction = fields.Boolean(
        string="Is Auction", compute="_compute_is_auction", store=True)
    invoice_count = fields.Integer(
        string="Invoices", compute="_compute_invoice_count")

    auction_stage = fields.Selection([
        ('template', 'Template'),
        ('auction', 'Auction'),
        ('sold', 'Sold')
    ], string="Auction Stage", default="template", tracking=True)

    auction_remaining_time = fields.Char(
        string="Remaining Time",
        compute="_compute_remaining_time",
        store=True
    )

    @api.depends('sale_type')
    def _compute_is_auction(self):
        for record in self:
            record.is_auction = (record.sale_type == 'auction')

    def action_start_auction(self):
        """ Start the auction process. """
        for record in self:
            if record.sale_type != 'auction':
                raise UserError("Only properties marked as 'Auction' can start the auction.")
            if record.auction_stage != 'template':
                raise UserError("Auction has already been started for this property.")
            if not record.auction_end_time:
                raise UserError("You must set an Auction End Time before starting the auction.")
            
            record.auction_stage = 'auction'

    def action_sold(self):
        """ Mark the property as sold to the highest bidder """
        for record in self:
            if record.auction_stage != 'auction':
                raise UserError("Auction must be in progress before marking as sold.")
            if not record.highest_bidder:
                raise UserError("No bids received. Cannot mark as sold.")
            
            record.auction_stage = 'sold'
            record.state = 'sold'
            record.buyer_id = record.highest_bidder
            record.selling_price = record.highest_offer
            record.create_invoice()

    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        """ Compute the highest offer and set the highest bidder """
        for record in self:
            highest_offer = max(record.offer_ids.mapped("price"), default=0.0)
            highest_bid = record.offer_ids.filtered(
                lambda o: o.price == highest_offer)
            record.highest_offer = highest_offer
            record.highest_bidder = highest_bid.partner_id if highest_bid else False

    @api.depends('auction_end_time')
    def _compute_remaining_time(self):
        """Compute the remaining time before auction ends."""
        for record in self:
            if not record.auction_end_time:
                record.auction_remaining_time = "Auction End Time Not Set"
            else:
                now = fields.Datetime.now()
                remaining_time = record.auction_end_time - now

                if remaining_time.total_seconds() <= 0:
                    record.auction_remaining_time = "Auction Ended"
                else:
                    days = remaining_time.days
                    hours, remainder = divmod(remaining_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    record.auction_remaining_time = (
                        f"{days}d {hours}h {minutes}m {seconds}s left" if days > 0
                        else f"{hours}h {minutes}m {seconds}s left" if hours > 0
                        else f"{minutes}m {seconds}s left"
                    )
    
    def get_auction_remaining_time(self):
        """ Calculate remaining auction time and return it as a string. """
        now = fields.Datetime.now()
        for record in self:
            if not record.auction_end_time:
                return "No Auction Set"
            
            remaining_time = record.auction_end_time - now
            if remaining_time.total_seconds() <= 0:
                return "Auction Ended"
            
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            return f"{days}d {hours}h {minutes}m {seconds}s left"

    def action_sold(self):
        """ Mark the property as sold to the highest bidder """
        for record in self:
            if record.auction_stage != 'in_progress':
                raise api.UserError(
                    "Auction must be in progress before marking as sold.")
            if not record.highest_bidder:
                raise api.UserError("No bids received. Cannot mark as sold.")
            record.auction_stage = 'sold'
            record.state = 'sold'
            record.buyer_id = record.highest_bidder
            record.selling_price = record.highest_offer
            record.create_invoice()

    def _compute_invoice_count(self):
        """ Compute the number of invoices related to the property """
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([
                ('partner_id', '=', record.buyer_id.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '!=', 'cancel'),
            ])
    def create_invoice(self):
        """ Generate an invoice when the property is sold """
        for record in self:
            if not record.buyer_id:
                raise ValueError("A buyer must be assigned before creating an invoice.")

            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'name': record.name,
                    'quantity': 1,
                    'price_unit': record.selling_price,
                })],
            }
            invoice = self.env['account.move'].create(invoice_vals)
            record.message_post(body=f"Invoice Created: <a href='/web#id={invoice.id}&model=account.move'>{invoice.name}</a>")
    def action_view_invoice(self):
        """ Opens the invoices related to the property """
        self.ensure_one()
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.buyer_id.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '!=', 'cancel'),
        ])
        
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('id', 'in', invoices.ids)],
            "context": {"create": False, 'default_move_type': 'out_invoice'},
            "name": _("Customer Invoices"),
            'view_mode': 'list,form',
        }