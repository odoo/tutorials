from odoo import api, fields, models


class EstatePropertyEvent(models.Model):
    _inherit = 'estate.property'

    event_id = fields.Many2one('event.event')

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)

        for rec in record:
            a = self.env['event.event'].create({
                'name': 'Open house event' + ' ' + rec.name,
                })
            rec.event_id = a.id

        return record

    def open_event(self):
        return {
                'name': 'Event',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'event.event',
                'res_id': self.event_id.id,
            }
