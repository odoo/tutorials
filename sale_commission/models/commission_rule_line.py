from odoo import fields, models


class CommissionRuleLine(models.Model):
    _name = 'commission.rule.line'
    _description = "Commission Rule Line"

    date = fields.Date(string="Date", default=fields.Date.today)
    user_id = fields.Many2one('res.users', string="User")
    team_id = fields.Many2one('crm.team', string="Sales Team")
    move_id = fields.Many2one('account.move', string="Invoice")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.move_id.company_id.currency_id)
    commission_rule_id = fields.Many2one('commission.rule', string="Rule")
    amount = fields.Monetary("Amount", required=True, currency_field='currency_id')
