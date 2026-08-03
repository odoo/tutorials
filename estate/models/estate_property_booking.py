from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "A model for estate property booking"

    property_id = fields.Many2one('estate.property', required=True)
    name = fields.Char(required=True)
    sales_person = fields.Many2one(
        "res.users",
    )
    customer = fields.Many2one("res.partner")
    time_slot = fields.Datetime(required=True)
    feedback = fields.Text()
    rating = fields.Selection(
        [
            ('high', "High"),
            ('medium', "Medium"),
            ('very_high', "Very High"),
        ],
    )

    @api.onchange('sales_person')
    def _onchange_sales_person(self):
        Booking = self.env['estate.property.booking']
        assigned_ids = Booking.search([]).mapped('sales_person.id')
        available_user = self.env['res.users'].search(
            [('id', 'not in', assigned_ids)],
            limit=1,
        )

        for record in self:
            if not record.sales_person:
                record.sales_person = available_user or self.env.user
                continue

            is_assigned = Booking.search_count(
                [('sales_person', '=', record.sales_person.id)],
            )

            if is_assigned:
                record.sales_person = available_user or False

                raise UserError(message="This sales person is already assigned.")

    @api.constrains("time_slot", "customer", "property_id")
    def _check_time_slot(self):
        for record in self:
            if not (record.property_id and record.customer and record.time_slot):
                continue

            domain = [
                ('id', '!=', record.id),
                ('property_id', '=', record.property_id.id),
                ('customer', '=', record.customer.id),
                ('time_slot', '=', record.time_slot),
            ]

            if self.env['estate.property.booking'].search_count(domain) > 0:
                raise UserError(
                    message='The selected time slot is already allocated for this customer and property.',
                )
