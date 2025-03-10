from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_multicompany = fields.Boolean(compute="_compute_is_multicompany")

    @api.depends('company_id')
    def _compute_is_multicompany(self):
        for record in self:
            user = self.env.user
            record.is_multicompany = len(user.company_ids) > 1

    def action_open_product_replenish(self):
        return {
            'name': "Low on stock? Let's replenish.",
            'type': 'ir.actions.act_window',
            'res_model': 'product.replenish',
            'view_mode': 'form',
            'view_id': self.env.ref('stock.view_product_replenish').id,
            'target': 'new',
            'context': {
                'default_product_id': self.product_variant_id.id if len(self.product_variant_ids) == 1 else False,
                'default_product_tmpl_id': self.id,
            },
        }
