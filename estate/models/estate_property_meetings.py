from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyMeeting(models.Model):
    _name = 'estate.property.meeting'
    _description = "Property Meeting"

    name = fields.Char(
    default='visit',
    )
    meeting_date = fields.Datetime(string="Meeting Date")

    property_id = fields.Many2one(
        string='property',
        comodel_name='estate.property',
        ondelete='restrict',
        required=True,
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('schedule', "schedule"),
            ('done', "done"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
        default='new',

    )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            existing = self.search([
                ('meeting_date', '=', vals.get('meeting_date')),
                ('property_id', '=', vals.get('property_id')),
            ])

            if existing:
                raise UserError(_("A meeting already exists at this time for this property."))

        return super().create(vals_list)

    @api.onchange('meeting_date')
    def _onchange_meeting_date(self):
        for rec in self:
            if rec.meeting_date and rec.state == 'new':
                rec.state = 'schedule'

    def done(self):
        for rec in self:
            rec.state = 'done'
            message = "Meeting completed"

        return {
            "effect": {
                "fadeout": "fast",
                "message": message,
                "img_url": "/web/static/img/smile.svg",
                "type": "rainbow_man",
            },
        }

    def cancel(self):
        for rec in self:
            if rec.state in ['schedule']:
                breakpoint()
                rec.state = 'cancelled'
            elif rec.state in ['done']:
                breakpoint()
                raise (_(" Cannot cancel a completed meeting "))
            else:
                breakpoint()
                raise UserError(_("You must schedule a meeting before cancelling it."))
