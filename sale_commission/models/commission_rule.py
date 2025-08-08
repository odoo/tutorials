from odoo import _, api, fields, models

class CommissionRule(models.Model):
    _name = 'commission.rule'

    comission_rate = fields.Integer(string="Commission Rate", required=True)
    commission_for = fields.Selection(
        selection=[
            ('salesperson', 'SalesPerson'),
            ('salesteam', 'Sales Team')
        ],
        string="Commission For",
        default='salesperson',
    )
    target_salesperson = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",)
    target_sales_team = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
    )
    product_category_id = fields.Many2one('product.category', string='Product Category')
    product_template_id = fields.Many2one('product.template', string='Product')
    max_discount = fields.Integer(string="Max Discount", required=True)
    salesperson = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",)
    sales_team = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
    )
    sequence = fields.Integer(string='Sequence', default=10)
    display_name = fields.Char(string="Condition", compute="_compute_display_name")
    @api.depends('product_template_id', 'product_category_id', 'max_discount', 'salesperson', 'sales_team')
    def _compute_display_name(self):
        for record in self:
            record.display_name = ""
            if record.product_template_id:
                record.display_name+=("Product: "+record.product_template_id.name)
            if record.product_category_id:
                record.display_name+=(" AND Category: "+record.product_category_id.display_name)
            if record.max_discount:
                record.display_name+=(" AND Max Discount: "+str(record.max_discount))
            if record.salesperson:
                record.display_name+=(" AND Salesperson: "+record.salesperson.name)
            if record.sales_team:
                record.display_name+=(" AND Team: "+record.sales_team.name)
            if record.display_name.startswith(" AND "):
                record.display_name = record.display_name[5:]
