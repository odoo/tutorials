from odoo import fields, models, api


class EstateProperty(models.Model):
    _inherit = "estate.property"

    event_ids = fields.One2many("event.event", "property_id", string="Events")
    event_count = fields.Integer(compute="_compute_event_count")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['event.event'].create({
                'name':  f'Open house - {record.name}',
                'organizer_id': record.salesperson_id.id,
                'property_id': record.id,
            })
        return records

    @api.depends("event_ids")
    def _compute_event_count(self):
        for record in self:
            record.event_count = len(record.event_ids)

    def action_view_events(self):
        for record in self:
            event = self.env['event.event'].search([('property_id', '=', record.id)])
            return {
                'type': 'ir.actions.act_window',
                'name': 'Event',
                'res_model': 'event.event',
                'view_mode': 'form',
                'res_id': event.id,
            }
