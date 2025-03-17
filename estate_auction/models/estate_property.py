from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    selling_mode = fields.Selection(
        selection=[
        ('regular', "Regular"),
        ('auction', "Auction"),
    ], default='regular', required=True)
    auction_end_time = fields.Datetime(string="End Time")
    highest_offer = fields.Float(string="Highest Offer", compute='_compute_highest_offer')
    highest_bidder = fields.Many2one('res.partner', string="Highest Bidder", compute='_compute_highest_offer')
    auction_stage = fields.Selection(
        selection=[
        ('template', "Template"),
        ('auction', "Auction"),
        ('done', "Done")
    ], string="Auction Stage", default='template', tracking=True)
    invoice_count = fields.Integer(string="Invoices", compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'property_id', string="Invoices")

    @api.depends('offer_ids.price', 'offer_ids.partner_id')
    def _compute_highest_offer(self):
        for record in self:
            if record.offer_ids:
                highest_offer = max(record.offer_ids, key=lambda o: o.price, default=None)
                record.highest_bidder = highest_offer.partner_id if highest_offer else False
                record.highest_offer = highest_offer.price if highest_offer else 0.0
            else:
                record.highest_bidder = False
                record.highest_offer = 0.0

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """Compute the number of invoices related to this property using the direct relation"""
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def action_view_invoices(self):
        """Open the related invoices using the direct relation"""
        self.ensure_one()

        # Find invoices related to this property
        invoice = self.env['account.move'].search([
            ('property_id', '=', self.id),
            ('move_type', '=', 'out_invoice')
        ])

        # Return action to view invoice
        action = {
            'name': _('Property Invoices'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id ,
            'context': {'create': False}
        }

        return action

    @api.onchange('selling_mode')
    def _onchange_selling_mode(self):
        if self.selling_mode == 'regular' and self.auction_stage != 'template':
            self.auction_stage = 'template'
            self.auction_end_time = False

    def action_sold(self):
        """
        Override action_sold to update the invoice with the property_id
        """
        # Call the parent method which returns the invoice
        invoice = super().action_sold()
        invoice.property_id = self.id

        # Log the invoice creation with property link
        self.message_post(
                body=_(("Invoice created with Id:%s and linked to this property") % (invoice.id))
            )
        return invoice

    def action_start_auction(self):
        """Start the auction process for this property"""
        self.ensure_one()
        if self.selling_mode == 'regular':
            raise UserError(_("This property is not marked for auction."))
            
        if not self.auction_end_time:
            raise UserError(_("Please set an end time for the auction."))

        if self.auction_end_time <= fields.Datetime.now():
            raise UserError(_("Auction end time must be in the future."))
        
        self.auction_stage = 'auction'

    def write(self, vals):
        if 'selling_mode' in vals and self.auction_stage in ['auction', 'done']:
            if vals['selling_mode'] == 'regular':
                raise UserError(_("Cannot change selling mode to 'Regular' when auction is in progress or completed."))

        return super(EstateProperty, self).write(vals)


    def check_auction_status(self):
        """
        Cron job to check if auctions have ended and process them
        This will run every 5 minutes
        """
        auction_properties = self.search([
            ('selling_mode', '=', 'auction'),
            ('state', 'in', ['new', 'offer_received']),
            ('auction_stage', '=', 'auction'),
            ('auction_end_time', '<=', fields.Datetime.now())
        ])

        for property in auction_properties:
            if property.offer_ids:
                highest_offer = property.offer_ids.filtered(lambda offer: offer.price == property.highest_offer)
                highest_offer.action_accept()

                property.write({
                    'auction_stage': 'done'
                })

                # Log the automatic acceptance
                property.message_post(
                    body=_(("Auction ended. Highest offer (%s) from %s was automatically accepted.") % 
                    (highest_offer.price, highest_offer.partner_id.name))
                )

            else:
                # No offers received, mark as auction ended
                property.write({
                    'auction_stage': 'done'  # Using the done stage even though it's cancelled
                })
                property.message_post(body=_("Auction ended with no offers."))
