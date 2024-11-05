from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    has_active_order = fields.Boolean("Has Active Order", compute='_compute_has_active_order', store=True)

    @api.depends('opportunity_ids')
    def _compute_has_active_order(self):
        for partner in self:
            partner.has_active_order = len(partner.opportunity_ids) > 0
