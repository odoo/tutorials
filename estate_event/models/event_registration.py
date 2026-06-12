from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def write(self, vals):
        res = super().write(vals)

        attended = (
            vals.get("state") == "done"
            or vals.get("attendance_state") == "attended"
        )
        if not attended:
            return res

        for reg in self:
            property_rec = reg.event_id.property_id
            if not property_rec:
                continue

            partner = reg.partner_id
            if not partner and reg.email:
                partner = self.env["res.partner"].search(
                    [("email", "=", reg.email)], limit=1
                ) or self.env["res.partner"].create({
                    "name": reg.name or reg.email,
                    "email": reg.email,
                })
        return res
