from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EventEvent(models.Model):
    _inherit = 'event.event'

    recurrency = fields.Boolean(
        string="Recurrency",
        default=False,
    )
    repeat_interval = fields.Integer(string="Repeat Every", default=1)
    repeat_type = fields.Selection([
        ('day', 'Daily'),
        ('week', 'Weeks'),
        ('month', 'Months'),
        ('year', 'Years'),

    ], default='day')

    repeat_until = fields.Selection([
        ('forever', "Forever"),
        ('end_date', "End date"),
        ('count', "Count")
    ], default='forever')

    end_date = fields.Date(string="End date")

    count = fields.Integer(string="Count")

    last_date = fields.Datetime(string="Last Date")

    @api.model
    def _create_recurring_events(self):
        recurring_events = self.env['event.event'].search([('recurrency', '=', True)])
        for event in recurring_events:
            interval = event.repeat_interval
            check_date = event.last_date or event.date_begin
            todays_date = fields.Datetime.today()
            orginal_start_time = event.date_begin.time()
            orginal_end_time = event.date_end.time()
            if (event.repeat_until == 'end_date' and event.end_date >= fields.Date.today()) or event.repeat_until == 'forever':
                if event.repeat_type == 'day':
                    if check_date.date() == (todays_date - relativedelta(days=interval)).date():
                        self.env['event.event'].create({
                            'name': event.name,
                            'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                            'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                            'recurrency': False
                        })
                        event.write({'last_date': todays_date})
                elif event.repeat_type == 'week':
                    if check_date.date() == (todays_date - relativedelta(weeks=interval)).date():
                        self.env['event.event'].create({
                            'name': event.name,
                            'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                            'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                            'recurrency': False
                        })
                        event.write({'last_date': todays_date})
                elif event.repeat_type == 'month':
                    if check_date.date() == (todays_date - relativedelta(months=interval)).date():
                        self.env['event.event'].create({
                            'name': event.name,
                            'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                            'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                            'recurrency': False
                        })
                        event.write({'last_date': todays_date})
                else:
                    if check_date.date() == (todays_date - relativedelta(years=interval)).date():
                        self.env['event.event'].create({
                            'name': event.name,
                            'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                            'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                            'recurrency': False
                        })
                        event.write({'last_date': todays_date})
            else:
                event_count = self.env['event.event'].search_count([('name', '=', event.name), ('recurrency', '=', False)])
                if event.count > event_count:
                    if event.repeat_type == 'day':
                        if check_date.date() == (todays_date - relativedelta(days=interval)).date():
                            self.env['event.event'].create({
                                'name': event.name,
                                'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                                'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                                'recurrency': False
                            })
                            event.write({'last_date': todays_date})
                    elif event.repeat_type == 'week':
                        if check_date.date() == (todays_date - relativedelta(weeks=interval)).date():
                            self.env['event.event'].create({
                                'name': event.name,
                                'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                                'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                                'recurrency': False
                            })
                            event.write({'last_date': todays_date})
                    elif event.repeat_type == 'month':
                        if check_date.date() == (todays_date - relativedelta(months=interval)).date():
                            self.env['event.event'].create({
                                'name': event.name,
                                'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                                'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                                'recurrency': False
                            })
                            event.write({'last_date': todays_date})
                    else:
                        if check_date.date() == (todays_date - relativedelta(years=interval)).date():
                            self.env['event.event'].create({
                                'name': event.name,
                                'date_begin': todays_date.replace(hour=orginal_start_time.hour, minute=orginal_start_time.minute, second=orginal_start_time.second),
                                'date_end': todays_date.replace(hour=orginal_end_time.hour, minute=orginal_end_time.minute, second=orginal_end_time.second),
                                'recurrency': False
                            })
                            event.write({'last_date': todays_date})
