from odoo import fields, models, api


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = "Sale Commission"

    date = fields.Date(required=True)
    user_id = fields.Many2one('res.users', string="Salesperson")
    team_id = fields.Many2one('crm.team', string="Sales Team")
    invoice_id = fields.Many2one('account.move')
    partner_id = fields.Many2one(related='invoice_id.partner_id', store=True)

    amount = fields.Monetary()
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id.id
    )

    rule_id = fields.Many2one('commission.rule')
    sale_order_id = fields.Many2one('sale.order')

    def check_commission_rules(self, sale_orders, invoice):
        # breakpoint()
        if not sale_orders:
            return
        rules = self.env['commission.rule'].search([
            ('active', '=', True)
        ])
        for order in sale_orders:
            for rule in rules:
                condition_ok = True
                if rule.salesperson_id and order.user_id != rule.salesperson_id:
                    condition_ok = False
                if rule.team_id and order.team_id != rule.team_id:
                    condition_ok = False

                if not condition_ok:
                    continue
                # existing = self.search([
                #     ('invoice_id', '=', invoice.id),
                #     ('rule_id', '=', rule.id),
                #     ('sale_order_id', '=', order.id)
                # ], limit=1)
                # if existing:
                #     continue
                commission_amount = invoice.amount_total * rule.commission_rate
                self.create({
                    'date': invoice.invoice_date,
                    'invoice_id': invoice.id,
                    'user_id': order.user_id.id,
                    'team_id': order.team_id.id,
                    'amount': commission_amount,
                    'rule_id': rule.id,
                    'sale_order_id': order.id,
                })
