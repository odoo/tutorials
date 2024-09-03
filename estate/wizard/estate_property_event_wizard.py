from odoo import models, fields, api

class EstatePropertyEventWizard(models.TransientModel):
    _name = 'estate.property.event.wizard'
    _description = 'Property Event Wizard'

    event_name = fields.Char(string="Event Name", required=True)
    date = fields.Datetime(string="Date", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    organizer_id = fields.Many2one('res.users', string="Organizer", default=lambda self: self.env.user)

    def create_event(self):
        self.env['calendar.event'].create({
            'name': self.event_name,
            'start': self.date,
            'stop': self.date,
            'allday': True,
            'user_id': self.organizer_id.id,
            'partner_ids': [(6, 0, self.attendee_ids.ids)],
        })
        return {'type': 'ir.actions.act_window_close'}
