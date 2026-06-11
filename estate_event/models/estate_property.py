from datetime import timedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    event_id = fields.Many2one('event.event', string="Event")

    @api.model
    def create(self, vals_list):
        properties = super().create(vals_list)
        for prop in properties:
            event = self.env['event.event'].create({
                'name': f"{prop.name} - Open House",
                'date_begin': fields.Datetime.now(),
                'date_end': fields.Datetime.now() + timedelta(hours=1),
                'is_published': True
            })
            prop.event_id = event.id
        return properties

    def action_open_events(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'form',
            'res_id': self.event_id.id,
        }
