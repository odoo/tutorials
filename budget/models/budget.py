from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError

class Budget(models.Model):
    _name = "budget.budget"
    _description = "Budget"
    _inherit = ['mail.thread']

    name = fields.Char('Budget Name', compute='_compute_budget_name', store=True)

    color= fields.Integer(default=5)
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')
    active= fields.Boolean(default=True)
    revision_id = fields.Many2one('budget.budget', string="Revision_id", readonly=True , tracking=True)
    is_favorite = fields.Boolean(default=False)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('revised', 'Revised'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, readonly=True, copy=False)
   

    on_over_budget = fields.Selection([
        ('warning', 'Show a warning'),
        ('restriction', 'Restrict on creation'),    
    ], string='Over Budget Policy',default="restriction")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    budget_lines = fields.One2many('budget.budget.lines', 'budget_id', 'Budget Lines', copy=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    analytic_account_ids = fields.Many2many('account.analytic.account')
    warnings = fields.Text(compute="_check_over_budget")

    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for record in self:
            if record.date_from == record.date_to:
                raise ValidationError("Start Date and End Date cannot be the same.")
            elif record.date_to < record.date_from:
                raise ValidationError("End Date must be after Start Date.")
            else:
                if record.state in ['draft', 'confirmed']:
                    overlapping_budgets = self.search([
                        ('id', '!=', record.id),  # Exclude the current record
                        ('state', 'in', ['draft', 'confirmed']),
                        ('date_from', '<=', record.date_to),
                        ('date_to', '>=', record.date_from),
                    ])
                    if overlapping_budgets:
                        raise UserError("Cannot create or update this budget because it overlaps with another budget")
    @api.depends("budget_lines.over_budget")
    def _check_over_budget(self):
        for record in self:
            if (
                record.on_over_budget == "warning"
                and any(ob > 0 for ob in record.budget_lines.mapped("over_budget")) > 0
            ):
                record.warnings = "Achieved amount exceeds the budget!"
            else:
                record.warnings = False

    @api.depends('date_from', 'date_to')
    def _compute_budget_name(self):
        for record in self:
            record.name = f"Budget:({record.date_from} to {record.date_to})"

    def action_budget_confirm(self):
        if self.state != 'draft':
            raise ValidationError("Only budgets in draft state can be confirmed.")
        self.write({'state': 'confirmed'})


    def action_budget_revise(self):
        if self.state != "confirmed":
            raise UserError("Only confirmed budgets can be revised.")
        self.ensure_one()
        new_budget_vals = self.copy_data()[0] 
        new_budget_vals['revision_id'] = self.id 
        new_budget_vals['state'] = 'draft'
      
        self.active = False
        self.state = 'revised'
        new_budget = self.create(new_budget_vals)
        self.message_post(
        body=f"The budget has been revised. A new draft budget has been created with ID {new_budget.id}.",
        subtype_xmlid="mail.mt_note"  
    )
    
        return new_budget
       

    def action_budget_draft(self):
        if self.state not in ['confirmed', 'revised']:
            raise ValidationError("Only confirmed or revised budgets can be set back to draft.")
        self.write({'state': 'draft'})    


    def action_budget_done(self):
        if self.state != 'revised':
            raise ValidationError("Only revised budgets can be marked as done.")
        self.write({'state': 'done'})        
