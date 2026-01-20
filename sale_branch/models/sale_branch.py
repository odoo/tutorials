from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleBranch(models.Model):
    _name = 'sale.branch'
    _description = 'Sale Branch'

    name = fields.Char(required=True, string='Branch Name')
    sequence_id = fields.Many2one('ir.sequence')
    code = fields.Char(required=True, string='Code')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            name = vals.get('name')
            code = vals.get('code')

            if not name or not code:
                raise UserError(
                    'Both "name" and "code" are required to create sequence.')

            sequence = self.env['ir.sequence'].create({
                'name': name,
                'code': code,
                'prefix': code + '/',
                'padding': 3
            })
            vals['sequence_id'] = sequence.id

        return super().create(vals_list)
