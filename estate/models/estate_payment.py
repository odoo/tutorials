from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePayment(models.Model):
    _name = 'estate.payment'
    _description = "Property Payment"
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(
        string="Payment Reference",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: "New",
        tracking=True,
    )
    booking_id = fields.Many2one(
        'estate.property.booking',
        string="Booking",
        required=True,
        tracking=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        related='booking_id.property_id',
        string="Property",
        store=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        related='booking_id.partner_id',
        string="Customer",
        store=True,
    )
    payment_type = fields.Selection(
        [
            ('booking', "Booking Amount"),
            ('remaining', "Remaining Amount"),
        ],
        string="Payment Type",
        required=True,
        default='booking',
        tracking=True,
    )
    payment_method = fields.Selection(
        [
            ('cash', "Cash"),
            ('bank_transfer', "Bank Transfer"),
            ('cheque', "Cheque"),
            ('card', "Card"),
        ],
        string="Payment Method",
        default='bank_transfer',
        tracking=True,
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        tracking=True,
    )
    payment_date = fields.Date(
        string="Payment Date",
        default=fields.Date.today,
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ('draft', "Draft"),
            ('paid', "Paid"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        default='draft',
        tracking=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code(
                        'estate.payment.sequence'
                    )
                    or 'New'
                )
        return super().create(vals_list)

    def action_confirm_payment(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError("Only draft payments can be confirmed.")

        self.write({'state': 'paid'})

        if self.payment_type == 'booking':
            self.booking_id.action_mark_booked()
        else:
            self.booking_id.action_mark_done()

        return True
