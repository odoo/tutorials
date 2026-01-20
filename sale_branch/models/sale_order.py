from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    branch_id = fields.Many2one('sale.branch', string='Branch')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            branch_id = vals.get('branch_id')
            if branch_id:
                branch = self.env['sale.branch'].browse(branch_id)
                if branch and branch.sequence_id:
                    vals['name'] = branch.sequence_id.next_by_id()
        return super().create(vals_list)
