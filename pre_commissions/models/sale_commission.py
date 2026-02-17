from odoo import models, fields


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = "Sale Commission"
    _order = 'date desc'

    date = fields.Date(required=True, default=fields.Date.context_today)

    user_id = fields.Many2one(
        'res.users', string="Salesperson", required=True, index=True)
    team_id = fields.Many2one('crm.team', string="Sales Team", index=True)
    invoice_id = fields.Many2one('account.move', string="Invoice", index=True)
    partner_id = fields.Many2one(
        related='invoice_id.partner_id', store=True, string="Customer")
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id, required=True)
    rule_id = fields.Many2one(
        'commission.rule', string="Commission Rule", required=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")

    def check_commission_rules(self, sale_orders, invoice):
        if not sale_orders or not invoice:
            return

        rules = self.env['commission.rule'].search(
            [('active', '=', True)],
            order='sequence asc'
        )

        commission_vals = []

        for order in sale_orders:
            for rule in rules:
                if not self._rule_applies(rule, order, invoice):
                    continue

                users, team = self._get_commission_owners(rule, order)
                if not users:
                    continue

                total_amount = invoice.amount_total * rule.commission_rate
                per_user_amount = (
                    total_amount / len(users)
                    if rule.commission_for == 'team'
                    else total_amount
                )

                for user in users:
                    commission_vals.append({
                        'date': invoice.invoice_date,
                        'invoice_id': invoice.id,
                        'user_id': user.id,
                        'team_id': team.id if team else user.sale_team_id.id,
                        'amount': per_user_amount,
                        'rule_id': rule.id,
                        'sale_order_id': order.id,
                    })

                break  # first valid rule wins

        if commission_vals:
            self.create(commission_vals)

    def _get_commission_owners(self, rule, order):
        if rule.commission_for == 'team' and order.team_id:
            users = order.team_id.member_ids.filtered(lambda u: u.active)
            return users, order.team_id

        if order.user_id:
            return order.user_id, False

        return self.env['res.users'], False

    def _rule_applies(self, rule, order, invoice):
        return all([
            self._rule_salesperson(rule, order),
            self._rule_team(rule, order),
            self._rule_products(rule, order),
            self._rule_discount(rule, order),
            self._rule_due_at(rule, invoice),
        ])

    def _rule_salesperson(self, rule, order):
        return not rule.salesperson_id or order.user_id == rule.salesperson_id

    def _rule_team(self, rule, order):
        return not rule.team_id or order.team_id == rule.team_id

    def _rule_products(self, rule, order):
        for line in order.order_line:
            if rule.product_id and line.product_id != rule.product_id:
                return False
            if rule.product_category_id and line.product_id.categ_id != rule.product_category_id:
                return False
        return True

    def _rule_discount(self, rule, order):
        if not rule.max_discount:
            return True
        return all(line.discount <= rule.max_discount for line in order.order_line)

    def _rule_due_at(self, rule, invoice):
        if rule.due_at == 'payment':
            return invoice.payment_state == 'paid'
        return True
