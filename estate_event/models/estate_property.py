from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    event_id = fields.Many2one(
        "event.event",
        string="Event",
        readonly=True,
        copy=False,
    )

    attended_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_attended_partner_ids",
        store=False,
    )

    def _compute_attended_partner_ids(self):
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
                        [("email", "=", registration.email)], limit=1
                    )
                        if not partner:
                            partner = self.env["res.partner"].create({
                            "name": registration.name or registration.email,
                            "email": registration.email,
                        })
                        partners |= partner

            done_visits = self.env["estate.property.visit"].search([
                ("property_id", "=", rec.id),
                ("state", "=", "done"),
            ])
            for visit in done_visits:
                if visit.partner_id:
                    partners |= visit.partner_id

            rec.attended_partner_ids = partners

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            event = self.env["event.event"].create({
                "name": rec.name,
                "date_begin": fields.Datetime.now(),
                "date_end": fields.Datetime.add(fields.Datetime.now(), hours=1),
                "property_id": rec.id,
            })
            rec.event_id = event.id
        return records

    def action_open_event(self):
        self.ensure_one()
        if not self.event_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "name": "Event",
            "res_model": "event.event",
            "view_mode": "form",
            "res_id": self.event_id.id,
            "target": "current",
        }
