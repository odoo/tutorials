from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    event_id = fields.Many2one('event.event', string='Event Id', copy=False)
    attendee_partner_ids = fields.Many2many('res.partner',
        compute='_compute_attendee_partner_ids',
        string='Event Attendees'
    )

    @api.depends(
    'event_id.registration_ids.partner_id',
    'event_id.registration_ids.state',
    'visit_ids.buyer_id',
    'visit_ids.state',
    )
    def _compute_attendee_partner_ids(self):
        for rec in self:
            partners = self.env["res.partner"]

            if rec.id and rec.event_id:
                for registration in rec.event_id.registration_ids:
                    is_attended = (
                        getattr(registration, 'attendance_state', '') == 'attended'
                        or registration.state == 'done'
                    )
                    if not is_attended:
                        continue
                    if registration.partner_id:
                        partners |= registration.partner_id
                    elif registration.email:
                        partner = self.env["res.partner"].search(
                            [("email", "=", registration.email)], limit=1)
                        if not partner:
                            partner = self.env["res.partner"].create({
                                "name": registration.name or registration.email,
                                "email": registration.email,
                            })
                        partners |= partner

            partners |= rec.visit_ids.filtered(lambda v: v.state == 'Done').mapped('buyer_id')
            rec.attendee_partner_ids = partners

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            event = self.env["event.event"].create({
                "name": f"Open House: {record.name}"
            })
            record.event_id = event
        return records

    def action_open_house_events(self):
        return {
            'name': 'Open House Event',
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'form',
            'res_id': self.event_id.id,
        }
