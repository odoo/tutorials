from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _description = 'Property Visit'
    _rec_name = 'property_id'

    property_id = fields.Many2one('estate.property', required=True, string="Property")
    user_id = fields.Many2one(related="property_id.sales_person_id", string="Salesperson")
    buyer_id = fields.Many2one('res.partner', required=True, string="Customer")
    schedule_date = fields.Datetime(required=True, string="Schedule Datetime")
    calendar_event_id = fields.Many2one('calendar.event', string="Calendar Event", ondelete='cascade')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='scheduled', copy=False)

    _unique_property_visit = models.Constraint(
        'UNIQUE("schedule_date", "property_id")', 'This date is already scheduled by an property.'
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            event = self.env['calendar.event'].create({
                'name': f"{rec.property_id.name} - {rec.buyer_id.name}",
                'start': rec.schedule_date,
                'stop': rec.schedule_date + relativedelta(hours=1),
                'user_id': rec.user_id.id,
                'partner_ids': [(4, rec.buyer_id.id)],
            })
            rec.calendar_event_id = event.id
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'schedule_date' in vals or 'user_id' in vals:
            for rec in self:
                if rec.calendar_event_id:
                    rec.calendar_event_id.write({
                        'start': rec.schedule_date,
                        'stop': rec.schedule_date + relativedelta(hours=1),
                        'user_id': rec.user_id.id,
                    })
        return res

    def action_set_done(self):
        self.state = 'done'

    def action_set_cancel(self):
        self.state = 'cancel'
