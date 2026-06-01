from odoo import models, api


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            partner = self.env['res.partner'].search([('email', '=', record.email)], limit=1)
            if not partner:
                partner = self.env['res.partner'].create({
                    'name': record.name,
                    'email': record.email,
                })
            record.partner_id = partner.id
        return records
