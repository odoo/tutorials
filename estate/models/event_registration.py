from odoo import models, api


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('partner_id') and vals.get('email'):

                partner = self.env['res.partner'].search([
                    ('email', '=', vals.get('email'))
                ], limit=1)

                if not partner:
                    partner = self.env['res.partner'].create({
                        'name': vals.get('name'),
                        'email': vals.get('email'),
                    })

                vals['partner_id'] = partner.id

        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)

        if 'name' in vals:
            for record in self:
                if record.partner_id:
                    record.partner_id.name = record.name

        return res
