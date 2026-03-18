from odoo import models, fields, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'


    partner_id = fields.Many2one(
        'res.partner',
        string="Customer"
    )

    def action_mark_attended(self):
        for rec in self:
            rec.is_attended = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('partner_id') and vals.get('name'):

                partner = self.env['res.partner'].create({
                    'name': vals.get('name'),
                    'email': vals.get('email'),
                    'phone': vals.get('phone'),
                })
                vals['partner_id'] = partner.id
        return super().create(vals_list)
