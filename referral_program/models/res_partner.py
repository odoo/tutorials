# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):

    _inherit = ['res.partner']

    referred_by = fields.Many2one(comodel_name='res.partner', domain="[('is_company', '=', False)]", tracking=True)
    is_referrer_readonly = fields.Boolean(compute="_compute_is_referrer_readonly")

    def _compute_is_referrer_readonly(self):
        for partner in self:
            if partner.referred_by:
                partner.is_referrer_readonly = not self.env.is_admin()
            else:
                partner.is_referrer_readonly = False

    def _is_cycle(self):
        visited = []
        start = self.referred_by
        while start:
            if start in visited:
                return True
            visited.append(start)
            start = start.referred_by
        return False

    @api.constrains('referred_by')
    def _check_valid_referral(self):
        if self._is_cycle():
            raise ValidationError(_("Cyclic referrals are not allowed."))
        if self.referred_by.phone:
            if self.phone==self.referred_by.phone:
                raise ValidationError(_("Customers with same phone number can't refer each other."))
        else:
            raise ValidationError(_("Referrer must have a mobile number."))

    @api.model
    def _load_pos_data_fields(self, config_id):
       data = super()._load_pos_data_fields(config_id)
       data += ['referred_by']
       return data
