from odoo import models, api, fields
from odoo.fields import Datetime as FieldsDatetime
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _inherit = "estate.property"

    event_id = fields.Many2one("event.event")

    @api.model
    def create(self, vals_list):
        records = super().create(vals_list)

        for rec in records:
            event = self.env["event.event"].create(
                {
                    "name": "Open House - " + rec.name,
                    "date_begin": FieldsDatetime.to_string(
                        datetime.today() + timedelta(days=1)
                    ),
                    "date_end": FieldsDatetime.to_string(
                        datetime.today() + timedelta(days=15)
                    ),
                    "property_id": rec.id,
                }
            )

            rec.event_id = event.id
        return records

    def action_open_event(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Event",
            "res_model": "event.event",
            "view_mode": "form",
            "res_id": self.event_id.id,
            "view_id": self.env.ref("event.view_event_form").id,
            "target": "current",
        }
