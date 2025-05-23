# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.fields import Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for record in self:
            product_templates = record.order_line.read(['product_template_id'])
            product_template_ids = [i['product_template_id'][0] for i in product_templates]
            product_categories_ids = [line.product_template_id.categ_id.id for line in record.order_line]
            commission_rule = self.env['commission.rule'].search([
    '&',
        '|',
        ('max_discount', '=', False),
        ('max_discount', '>=', self.reward_amount),
        '&',
            '&',
                '|',
                    ('product_template_id', '=', False),
                    ('product_template_id', 'in', product_template_ids),
                '|',
                    ('product_category_id', '=', False),
                    ('product_category_id', 'in', product_categories_ids),
            '&',
                '|',
                    ('salesperson', '=', False),
                    ('salesperson', '=', self.user_id.id),
                '|',
                    ('sales_team', '=', False),
                    ('sales_team', '=', self.team_id.id),
            ])
            commission_product = self.env['product.product'].search([('name', '=', 'commission')])
            if not commission_product:
                commission_product = self.env['product.product'].create({'name': 'commission'})
            if commission_rule:
                for rule in commission_rule:
                    commission_product.list_price = rule.comission_rate*self.amount_total*0.01
                    if rule.commission_for == 'salesperson':
                        new_invoice = self.env['account.move'].create({
                            'partner_id': rule.target_salesperson.partner_id.id,
                            'move_type': 'out_invoice',
                            'invoice_line_ids': [
                                Command.create({
                                    'product_id': commission_product.id,
                                })
                            ],
                        })
                        new_invoice.action_post()
                        self.env['commission.list'].create({
                            'date': new_invoice.invoice_date,
                            'salesperson': rule.target_salesperson.id,
                            'invoice': new_invoice.display_name,
                            'Amount': new_invoice.amount_total,
                        })
                    else:
                        team_user = self.env['res.partner'].search([('name', '=', rule.target_sales_team.name)])
                        if not team_user:
                            team_user = self.env['res.partner'].create({
                                'name': rule.target_sales_team.name,
                            })
                        new_invoice = self.env['account.move'].create({
                            'partner_id': team_user.id,
                            'move_type': 'out_invoice',
                            'invoice_line_ids': [
                                Command.create({
                                    'product_id': commission_product.id,
                                })
                            ],
                        })
                        new_invoice.action_post()
                        self.env['commission.list'].create({
                            'date': new_invoice.invoice_date,
                            'sales_team': rule.target_sales_team.id,
                            'invoice': new_invoice.display_name,
                            'Amount': new_invoice.amount_total,
                        })
        super().action_confirm()

