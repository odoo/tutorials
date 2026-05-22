from odoo import models


class EstatePropertyEventRegister(models.Model):
    _inherit = 'event.registration'

    def action_set_done(self):
        res = super().action_set_done()
        if self.event_id.registration_ids:
            for rec in self:
                a = self.env['res.partner'].create({
                    'name': rec.name,
                    'email': rec.email
                    })
                rec.partner_id = a.id

            return res
