from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "Real Estate Booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    property_id = fields.Many2one("estate.property", string="property", required=True, copy=True, readonly=True)
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    payment_ids = fields.One2many("estate.property.payments", "booking_id", string="payment")
    booking_amount = fields.Float(string="Booking Amount", compute="_compute_booking_amount", store=True)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.today)
    remaining_amount = fields.Float(string="total amount left", compute="_compute_remaining_amount")
    offer_id = fields.Many2one("estate.property.offer", string="offer")
    deadline = fields.Datetime(
        string="Deadline",
        default=lambda self: fields.Datetime.now() + timedelta(days=7),
    )
    payment_type = fields.Selection(
            selection=[
                ('installments', "Installments"),
                ('full_payments', "Full Payments"),
            ],
        )
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('cancelled', "Cancelled"),
            ('confirmed', "Confirmed"),
        ],
        string="state of booking",
        default='draft',
    )

    @api.depends('property_id.best_price')
    def _compute_booking_amount(self):
        for record in self:
            exp_price = record.property_id.best_price
            record.booking_amount = (0.10 * exp_price)

    @api.depends('property_id.best_price', 'booking_amount', 'payment_ids.amount', 'payment_ids.status')
    def _compute_remaining_amount(self):
        for record in self:
            paid = sum(record.payment_ids.filtered(lambda o: o.status == 'paid').mapped('amount'))
            record.remaining_amount = record.property_id.best_price - paid - record.booking_amount
            # if record.payment_ids:
            #     record.remaining_amount = record.property_id.best_price - (record.booking_amount + record.payment_ids.amount)
            # else:
            #     record.remaining_amount = record.property_id.best_price - record.booking_amount

    @api.depends('property_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.property_id.name

    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals:
            for booking_id in self:
                if booking_id.state == 'confirmed':
                    template = self.env.ref('estate.estate_booking_confirmed_mail_template')
                    template.send_mail(booking_id.id, force_send=True)
                if booking_id.state == 'cancelled':
                    booking_id.property_id.state = 'offer_received'
                    if booking_id.offer_id:
                        booking_id.offer_id.status = 'Refused'
                        booking_id.payment_ids.filtered(lambda p: p.status in ('pending', 'paid')).write({'status': 'cancelled'})
        return res
