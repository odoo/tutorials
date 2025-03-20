# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    is_selected = fields.Boolean(string="Selected Address", default=False)
    show_in_contact_detail = fields.Boolean(string="Show in Contact Detail", default=True)

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        lead_id = self.env.context.get('default_lead_id')
        type = self.env.context.get('default_type')
        company_type = self.env.context.get('default_company_type')
        parent_id = self.env.context.get('default_parent_id')
        if lead_id:
            defaults.update(
                parent_id=parent_id,
                type=type,
                company_type=company_type,
                user_id=self.env.user.id,
            )
        return defaults

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        for partner, vals in zip(partners, vals_list):
            if partner.type == 'contact' and partner.parent_id:
                vals['parent_id'] = partner.parent_id.id
                partner._fields_sync(vals)
        return partners
