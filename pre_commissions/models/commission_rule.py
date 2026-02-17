from odoo import fields, models, api


class CommisionRule(models.Model):
    _name = 'commission.rule'
    _description = "Commission Rule"
    _order = 'sequence'

    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    commission_rate = fields.Float(required=True)
    due_at = fields.Selection([
        ('invoice', "Invoice Posted"),
        ('payment', "Payment Received")
    ], default='invoice', required=True)
    commission_for = fields.Selection([
        ('salesperson', "Salesperson"),
        ('team', "Sales Team")
    ])
    product_id = fields.Many2one(
        'product.product')
    product_category_id = fields.Many2one('product.category')
    product_expired = fields.Selection([
        ('no_impact', 'No Impact'),
        ('yes', "Expired Only"),
        ('no', 'Not Expired')
    ], default='no_impact')
    max_discount = fields.Float(string="Max Discount %")
    fast_payment = fields.Boolean()
    fast_payment_days = fields.Integer()
    salesperson_id = fields.Many2one('res.users')
    team_id = fields.Many2one('crm.team', string="Sales Team")
    condition_display = fields.Char(
        compute='_compute_condition_display',
        store=True
    )

    @api.onchange('commission_for')
    def _onchange_commission_for(self):
        for rec in self:
            if rec.commission_for == 'salesperson':
                rec.team_id = False
            elif rec.commission_for == 'team':
                rec.salesperson_id = False
            else:
                rec.salesperson_id = False
                rec.team_id = False

    @api.depends(
        'product_category_id',
        'product_id',
        'salesperson_id',
        'team_id',
        'max_discount',
        'product_expired'
    )
    def _compute_condition_display(self):
        for rec in self:
            parts = []

            if rec.product_id:
                parts.append(f"Product: {rec.product_id.name}")
            rec.product_category_id = rec.product_category_id or rec.product_id.categ_id

            if rec.product_category_id:
                parts.append(f"Category: {rec.product_category_id.name}")

            if rec.salesperson_id:
                parts.append(f"Salesperson: {rec.salesperson_id.name}")

            if rec.team_id:
                parts.append(f"Team: {rec.team_id.name}")

            if rec.max_discount:
                parts.append(f"Max Discount: {rec.max_discount}%")

            if rec.product_expired != 'no_impact':
                selection = dict(
                    rec.fields_get(['product_expired'])[
                        'product_expired']['selection']
                )
                label = selection.get(rec.product_expired)
                parts.append(f"Product Expiry: {label}")

            rec.condition_display = " AND ".join(parts) if parts else "All"
