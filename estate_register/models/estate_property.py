from odoo import models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_set_done(self):
        super().action_set_done()
        new_partner = self.env['res.partner'].create({
            'name': self.name,
        })
        self.partner_id = new_partner.id
