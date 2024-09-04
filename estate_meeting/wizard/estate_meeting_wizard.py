from odoo import fields, models


class OfferWizard(models.TransientModel):
    _name = "estate.meeting.wizard"
    _description = "estate property meeting wizard"

    agenda = fields.Text()
    start_date = fields.Date()
    end_date = fields.Date()
    description = fields.Text()
    duration = fields.Float()

    def action_schedule_meeting(self):
        context = self.env.context
        active_ids = context.get('active_ids', [])
        property_id = self.env['estate.property'].browse(active_ids)
        salesman = property_id.salesman_id
        print(context)
        self.env['calendar.event'].create({
                'name': self.agenda,
                'start': self.start_date,
                'stop': self.end_date,
                'description': self.description,
                'duration': self.duration,
                'partner_ids': [(6, 0, [salesman.partner_id.id])]
            })
