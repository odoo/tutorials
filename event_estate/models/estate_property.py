from datetime import timedelta

from odoo import models, fields, api


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    event_id = fields.Many2one('event.event', string="Open House Event")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            event = self.env['event.event'].create({
                'name': f"Open House - {record.name}",
                'date_begin': fields.Datetime.now(),
                'date_end': fields.Datetime.now() + timedelta(hours=2),
                'property_id': record.id,
            })
            record.event_id = event.id
        return records

    def action_view_event(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Event',
            'res_model': 'event.event',
            'view_mode': 'form',
            'res_id': self.event_id.id,
        }
