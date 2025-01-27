from odoo import fields, models, api
from datetime import timedelta, date

class BudgetCreate(models.TransientModel):
    _name = 'budget.main'
    _description = "Create budget"

    start_date = fields.Date(required=True)
    end_date = fields.Date(index=True)
    periods = fields.Selection(
        [
            ('monthly', 'Monthly'),
            ('quaterly', 'Quaterly')
        ],
        default="monthly"
    )
    analytic_account_ids = fields.Many2many('account.analytic.account', required=True)

    @api.model_create_multi         # Override Create Method For create budget 
    def create(self, vals_list):
        budget_main = super(BudgetCreate, self).create(vals_list)

        start_date = budget_main.start_date
        end_date = budget_main.end_date
        periods = budget_main.periods

        if periods == 'monthly':
            current_date = start_date
            while current_date <= end_date:
                next_month = current_date.replace(day=28) + timedelta(days=4)  
                month_end_date = next_month - timedelta(days=next_month.day)
                
                budget_name = f"Budget: {current_date.strftime('%Y-%m-%d')} to {month_end_date.strftime('%Y-%m-%d')}"

                self.env['budget.budget'].create({
                    'name': budget_name,
                    'period_start_date': current_date,
                    'period_end_date': month_end_date,
                })
                
                current_date = month_end_date + timedelta(days=1)

        elif periods == 'quaterly':
            if (end_date - start_date).days < 90:
                current_date = start_date
                while current_date <= end_date:
                    next_month = current_date.replace(day=28) + timedelta(days=4) 
                    month_end_date = next_month - timedelta(days=next_month.day)
                    
                    budget_name = f"Budget: {current_date.strftime('%Y-%m-%d')} to {month_end_date.strftime('%Y-%m-%d')}"
                    self.env['budget.budget'].create({
                        'name': budget_name,
                        'period_start_date': current_date,
                        'period_end_date': month_end_date,
                    })

                    current_date = month_end_date + timedelta(days=1)
            else:
                current_date = start_date
                while current_date <= end_date:
                    if current_date.month in [1, 2, 3]:
                        quarter_end_date = date(current_date.year, 3, 31)
                    elif current_date.month in [4, 5, 6]:
                        quarter_end_date = date(current_date.year, 6, 30)
                    elif current_date.month in [7, 8, 9]:
                        quarter_end_date = date(current_date.year, 9, 30)
                    else:
                        quarter_end_date = date(current_date.year, 12, 31)

                    budget_name = f"Budget: {current_date.strftime('%Y-%m-%d')} to {quarter_end_date.strftime('%Y-%m-%d')}"
                    self.env['budget.budget'].create({
                        'name': budget_name,
                        'period_start_date': current_date,
                        'period_end_date': quarter_end_date,
                    })
                    
                    current_date = quarter_end_date + timedelta(days=1)

        return budget_main
