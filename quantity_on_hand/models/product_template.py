from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_multicompany = fields.Boolean(compute="_compute_is_multicompany")

    @api.depends('company_id')
    def _compute_is_multicompany(self):
        for record in self:
            record.is_multicompany = len(self.env.user.company_ids) > 1
