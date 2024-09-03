import logging
from datetime import datetime, timedelta
from odoo import api, fields, models


class EstateMeetings(models.TransientModel):
    _name = "estate.meetings"
    _description = "Estate Meeting"

    @api.model
    def default_get(self, fields_list):
        # breakpoint()
        res = super().default_get(fields_list)
        proper_id = self.env.context["active_id"]
        logging.info(proper_id)
        proper = self.env["estate.property"].browse(proper_id)
        logging.info(proper)
        partner = self.env["res.partner"].browse(proper.salesman_id.partner_id.id)
        logging.info(partner)
        # salsesman =
        # res["attendee_ids"] = proper.salesman_id.id
        res["attendee_ids"] = partner
        logging.info(res)
        return res

    @api.model
    def _default_start(self):
        now = fields.Datetime.now()
        return now + (datetime.min - now) % timedelta(minutes=30)

    @api.model
    def _default_stop(self):
        now = fields.Datetime.now()
        start = now + (datetime.min - now) % timedelta(minutes=30)
        return start + timedelta(hours=1)

    name = fields.Char("Meeting Subject", required=True)
    description = fields.Html("Description")
    user_id = fields.Many2one(
        "res.users", "Organizer", default=lambda self: self.env.user
    )
    start = fields.Datetime(
        "Start",
        required=True,
        tracking=True,
        default=_default_start,
        help="Start date of an event, without time for full days events",
    )
    stop = fields.Datetime(
        "Stop",
        required=True,
        tracking=True,
        default=_default_stop,
        compute="_compute_stop",
        readonly=False,
        store=True,
        help="Stop date of an event, without time for full days events",
    )
    duration = fields.Float(
        "Duration", compute="_compute_duration", store=True, readonly=False
    )
    allday = fields.Boolean("All Day", default=False)
    attendee_ids = fields.Many2one("res.partner", readyonly=True)

    def _get_duration(self, start, stop):
        """Get the duration value between the 2 given dates."""
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)

    @api.depends("stop", "start")
    def _compute_duration(self):
        for event in self:
            event.duration = self._get_duration(event.start, event.stop)

    @api.depends("start", "duration")
    def _compute_stop(self):
        duration_field = self._fields["duration"]
        self.env.remove_to_compute(duration_field, self)
        for event in self:
            # Round the duration (in hours) to the minute to avoid weird situations where the event
            # stops at 4:19:59, later displayed as 4:19.
            event.stop = event.start and event.start + timedelta(
                minutes=round((event.duration or 1.0) * 60)
            )
            if event.allday:
                event.stop -= timedelta(seconds=1)

    def action_create_meeting(self):
        logging.info(self.attendee_ids)
        self.env["calendar.event"].create(
            {
                "name": self.name,
                "description": self.description,
                "user_id": self.user_id.id,
                "start": self.start,
                "stop": self.stop,
                "allday": self.allday,
                "partner_ids": self.attendee_ids,
            }
        )
