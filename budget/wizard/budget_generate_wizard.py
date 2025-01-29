from odoo import models, fields
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class BulkBudgetGenerate(models.TransientModel):
    _name="budget.bulk.wizard"
    
    date_start              =       fields.Date     ( string = "From", required = True )
    date_end                =       fields.Date     ( string = "to", required = True )
    period                  =       fields.Selection( string = "Periods", default="monthly", selection=[('monthly', 'Monthly'), ('quaterly', 'Quaterly')])
    analytic_account_ids    =       fields.Many2many ( string="Analytic Account", comodel_name="account.analytic.account", required=True)

    
    def _is_budget_safe_to_create(self, starting_date, ending_date):
        existing_budget = self.env['budget.budget'].search([
                ("date_start", "=", starting_date.strftime('%Y-%m-%d')),
                ("date_end", "=", ending_date.strftime('%Y-%m-%d')),
                ("active", "!=", False),  # skip the archived budgets
            ]
        )

        if existing_budget:
            return False
        return True
    
    def action_create_bulk_budget(self):
        start_date = self.date_start
        end_date   = self.date_end
        period_type= self.period
        
        current_date = start_date
        
        unsuccesful_budgets= []
        
        while current_date <= end_date:

            starting_date = current_date.replace(day=1)
            ending_date = starting_date + relativedelta(months=1, days=-1)
            
            if period_type == 'quaterly':
                ending_date = starting_date + relativedelta(months=3, days=-1)
            
            can_create= self._is_budget_safe_to_create(starting_date, ending_date)
            if(can_create):
                budget_id= self.env['budget.budget'].create({
                    'date_start': starting_date,
                    'date_end': ending_date,
                    'responsible_id': self.env.user.id,
                    'name': f"Budget: {starting_date.strftime('%m/%d/%Y')} to {ending_date.strftime('%m/%d/%Y')}",
                })
                
                budget_line_ids= []
                for account_id in self.analytic_account_ids:
                    line_id= self.env['budget.budget.line'].create({
                        'budget_amount':0,
                        'analytic_account_id': account_id.id,
                        'budget_id': budget_id.id
                    })
                    budget_line_ids.append(line_id.id)
                
                budget_id.update({
                    'budget_line_ids': budget_line_ids
                })
            else:
                unsuccesful_budgets.append(f"Budget: {starting_date.strftime('%m/%d/%Y')} to {ending_date.strftime('%m/%d/%Y')}")

            if period_type == 'monthly':
                current_date += relativedelta(months=1)
            elif period_type == 'quaterly':
                current_date += relativedelta(months=3)

        if(len(unsuccesful_budgets) > 0):
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'skipped existing budgets',
                    'type': 'warning',
                    'message': unsuccesful_budgets.__str__(),
                    'sticky': False,
                    "next": {"type": "ir.actions.act_window_close"} #necesarry to close any opened action window
                }
            }
            return notification
        return True

   