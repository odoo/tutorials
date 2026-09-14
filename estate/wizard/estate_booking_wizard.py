from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateBookingWizard(models.TransientModel):
    _name = 'estate.booking.wizard'
    _description = "Book Property Wizard"

    property_id = fields.Many2one(
        'estate.property',
        required=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
    )
    sold_price = fields.Float(
        related='property_id.selling_price',
        readonly=True,
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

    @api.depends('sold_price', 'booking_percentage')
    def _compute_amounts(self):
        for wizard in self:
            wizard.booking_amount = (
                wizard.sold_price * wizard.booking_percentage
            ) / 100.0

            wizard.remaining_amount = (
                wizard.sold_price - wizard.booking_amount
            )

    def action_confirm_booking(self):
        self.ensure_one()

        property = self.property_id

        if property.state != 'offer_accepted':
            raise UserError(
                "Only an accepted property can be booked."
            )

        active_booking = self.env['estate.property.booking'].search_count(
            [
                ('property_id', '=', property.id),
                ('state', 'in', ('draft', 'booked')),
            ]
        )
        if active_booking:
            raise UserError(
                "This property already has an active booking."
            )

        booking = self.env['estate.property.booking'].create({
            'property_id': property.id,
            'partner_id': self.partner_id.id,
            'sold_price': self.sold_price,
            'booking_percentage': self.booking_percentage,
            'booking_amount': self.booking_amount,
            'remaining_amount': self.remaining_amount,
            'state': 'draft',
        })

        return {
            'type': 'ir.actions.act_window',
            'name': "Booking",
            'res_model': 'estate.property.booking',
            'view_mode': 'form',
            'res_id': booking.id,
            'target': 'current',
        }
