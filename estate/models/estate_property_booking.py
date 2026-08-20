from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyBooking(models.Model):
    _name = 'estate.property.booking'
    _description = "Property Booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string="Booking Details",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: "New",
        tracking=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        tracking=True,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        related='property_id.salesperson_id',
        store=True,
    )
    sold_price = fields.Float(
        related='property_id.selling_price',
        required=True,
        tracking=True,
    )
    booking_percentage = fields.Float(
        default=10.0,
    )
    booking_amount = fields.Float(
        compute='_compute_amounts',
        store=True,
    )
    remaining_amount = fields.Float(
        compute='_compute_amounts',
        store=True,
    )
    payment_ids = fields.One2many(
        'estate.payment',
        'booking_id',
        string="Payments",
    )
    booking_date = fields.Date(
        default=fields.Date.today,
    )
    state = fields.Selection(
        [
            ('draft', "Draft"),
            ('booked', "Booked"),
            ('done', "Done"),
            ('cancel', "Cancelled"),
        ],
        default='draft',
        tracking=True,
    )
    notes = fields.Text()

    @api.depends('sold_price', 'booking_percentage')
    def _compute_amounts(self):
        for rec in self:
            rec.booking_amount = (
                rec.sold_price * rec.booking_percentage
            ) / 100

            rec.remaining_amount = (
                rec.sold_price - rec.booking_amount
            )

    @api.onchange('property_id')
    def _onchange_property_id(self):
        if self.property_id:
            self.partner_id = self.property_id.buyer_id
        else:
            self.partner_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code(
                        'estate.booking.sequence'
                    )
                    or 'New'
                )
        return super().create(vals_list)

    def action_pay_booking_amount(self):
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(
                "Booking amount can only be paid for draft bookings."
            )

        pending = self.payment_ids.filtered(
            lambda p: p.payment_type == 'booking' and p.state == 'draft'
        )
        if pending:
            raise UserError(
                "A booking amount payment is already pending."
            )

        payment = self.env['estate.payment'].create({
            'booking_id': self.id,
            'payment_type': 'booking',
            'amount': self.booking_amount,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': "Booking Amount Payment",
            'res_model': 'estate.payment',
            'view_mode': 'form',
            'res_id': payment.id,
            'target': 'current',
        }

    def action_mark_booked(self):
        self.ensure_one()

        self.write({
            'state': 'booked',
        })

        self.property_id.write({
            'state': 'booked',
            'booking_id': self.id,
        })

    def action_pay_remaining_amount(self):
        self.ensure_one()

        if self.state != 'booked':
            raise UserError(
                "Remaining amount can only be paid for booked properties."
            )

        pending = self.payment_ids.filtered(
            lambda p: p.payment_type == 'remaining' and p.state == 'draft'
        )
        if pending:
            raise UserError(
                "A remaining amount payment is already pending."
            )

        payment = self.env['estate.payment'].create({
            'booking_id': self.id,
            'payment_type': 'remaining',
            'amount': self.remaining_amount,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': "Remaining Amount Payment",
            'res_model': 'estate.payment',
            'view_mode': 'form',
            'res_id': payment.id,
            'target': 'current',
        }

    def action_mark_done(self):
        self.ensure_one()

        self.write({
            'state': 'done',
        })

        if self.property_id:
            self.property_id.action_sold()

    def action_cancel_booking(self):
        self.ensure_one()

        if self.state == 'done':
            raise UserError("A completed booking cannot be cancelled.")

        if self.state == 'cancel':
            raise UserError("This booking is already cancelled.")

        # paid_booking_payment = self.payment_ids.filtered(
        #     lambda p: p.payment_type == 'booking' and p.state == 'paid'
        # )
        # if paid_booking_payment:
        #     raise UserError(
        #         "Booking amount is already paid, this booking cannot be cancelled."
        #     )

        self.payment_ids.filtered(
            lambda p: p.state == 'draft'
        ).write({
            'state': 'cancel',
        })

        self.write({
            'state': 'cancel',
        })

        self.property_id.write({
            'state': 'offer_received',
            'booking_id': False,
            'buyer_id': False,
        })

        self.property_id.offer_ids.write({
            'status': False,
        })
