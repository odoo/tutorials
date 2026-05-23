from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def write(self, vals):
        res = super().write(vals)
        attended = (vals.get("attendance_state") == "attended"
        or vals.get("state") == "done")
        if attended:
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
                if not partner:
                    continue
                self.env["estate.property.offer"].search([
                    ("property_id", "=", property_rec.id),
                    ("partner_id", "=", partner.id),
                ], limit=1)
        return res
