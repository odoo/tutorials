from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        """Overrides invoice posting to trigger commission calculation."""
        res = super()._post(soft)

        self.filtered(
            lambda m:
                m.move_type == 'out_invoice'
                and (m.invoice_user_id or m.team_id)
        )._create_commission_rule_lines('invoicing')

        return res

    def action_register_payment(self):
        """Overrides payment registration to trigger commision calculation."""
        res = super().action_register_payment()
        commission_lines = self._get_applicable_commission()
        self.filtered(
            lambda m: (
                m.move_type == 'out_invoice'
                and (m.invoice_user_id or m.team_id)
                and m not in commission_lines.move_id
            )
        )._create_commission_rule_lines('payment')
        return res

    def _get_applicable_commission(self):
        """Check if a commission entry already exists for recordset."""
        return self.env['commission.rule.line'].search_fetch(
            [('move_id', 'in', self.ids)],
            ['move_id']
        )

    def _create_commission_rule_lines(self, trigger_stage):
        for move in self:
            commission_rules = self.env['commission.rule'].search([
                ('due_at', '=', trigger_stage),  
                ('product_id', 'in', move.invoice_line_ids.product_id.ids + [False]),
                ('product_category_id', 'in', move.invoice_line_ids.product_id.categ_id.ids + [False]),
                ('user_id', 'in', [move.invoice_user_id.id ,False]),
                ('team_id', 'in', [move.invoice_user_id.sale_team_id.id, False]),
            ])

            person_rule = self.env['commission.rule']
            team_rule = self.env['commission.rule']

            for rule in commission_rules:
                if rule.commission_for == 'person' and not person_rule:
                    person_rule = rule
                if rule.commission_for == 'team' and not team_rule:
                    team_rule = rule
                if person_rule and team_rule:
                    break

            commission_rule_lines = [{
                    'date': move.invoice_date,
                    'user_id': rule.user_id.id,
                    'team_id': rule.team_id.id,
                    'move_id': move.id,
                    'amount': move.amount_total * (rule.rate),
                    'currency_id': move.currency_id.id,
                    'commission_rule_id' : rule.id,
                }
                for rule in (person_rule, team_rule)
            ]
            if commission_rule_lines:
                self.env['commission.rule.line'].create(commission_rule_lines)
