# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    referrer = fields.Boolean(string='Referrer', default=False)
    referred_by = fields.Many2one(
        'res.partner',
        string='Referred By',
        help='The person who referred this partner',
        tracking=True,
    )
    referral_status = fields.Selection(
        selection=[
            ('editable', 'Editable'),
            ('locked', 'Locked'),
        ],
        compute='_compute_referral_status'
    )

    @api.depends('referred_by')
    def _compute_referral_status(self):
        for record in self:
            if self.env.user.has_group('base.group_system'):
                record.referral_status = 'editable'
            elif record.referred_by and record.id:
                record.referral_status = 'locked'
            else:
                record.referral_status = 'editable'

            if record.id and record.referred_by:
                record.referred_by.referrer = True

    @api.constrains('referred_by')
    def _check_referrer_not_referred(self):
        for record in self:
            if record.referred_by and record.referrer:
                raise ValidationError("A referrer cannot be referred by another person.")
            if record.referred_by == record:
                raise ValidationError("A person cannot refer themselves.")

    @api.onchange('company_type')
    def _onchange_company_type(self):
        if self.company_type == 'company':
            self.referred_by = False

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('referred_by')
        return fields
