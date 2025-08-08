from odoo import _, api, fields, models

class SaleCommission(models.Model):
    _name = 'commission.list'

    date = fields.Date(string="Date")
    salesperson = fields.Many2one(
        comodel_name='res.users',
        string="User",)
    sales_team = fields.Many2one(
        comodel_name='crm.team',
        string="Team",
    )
    invoice = fields.Char(string="Invoice")
    Amount = fields.Integer(string="Amount")
    display_amount = fields.Char(compute="_compute_display_amount")
    @api.depends('Amount')
    def _compute_display_amount(self):
        for record in self:
            record.display_amount = str(record.Amount)+str(self.env.company.currency_id.symbol)
