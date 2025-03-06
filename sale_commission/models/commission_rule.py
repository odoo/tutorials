from odoo import _, api, fields, models


class CommissionRule(models.Model):
    _name = 'commission.rule'
    _description = "Commission Rule"

    sequence = fields.Integer('Sequence', default=1, help="Used to order commission rule.")
    rate = fields.Float(string="Commission Rate", required=True)
    commission_for = fields.Selection(
        selection=[
            ('person', "Salesperson"),
            ('team', "Sales Team")
        ],
        string="Commission for",
        required=True,
        default='person'
    )
    due_at = fields.Selection(
        selection=[
            ('invoicing', "Invoicing"),
            ('payment', "Payment"),
        ],
        string="Due at",
        required=True,
    )
    product_expired = fields.Selection(
        selection=[
            ('no_impact', "No Impact"),
            ('yes', "Yes"),
            ('no', "No")
        ],
        string="Product Expired",
        required=True
    )
    max_discount = fields.Float(string="Max Discount")
    on_fast_payment = fields.Boolean(string="On Fast Payment")
    fast_payment_days = fields.Integer(string="Before Days")
    display_name = fields.Char(string="Condition", compute="_compute_display_name", store=True)

    product_category_id = fields.Many2one('product.category', string="Product Category")
    product_id = fields.Many2one('product.product', string="Product")
    user_id = fields.Many2one('res.users', string="Salesperson")
    team_id = fields.Many2one('crm.team', string="Sales Team")

    @api.depends('product_category_id', 'product_id', 'team_id', 'user_id')
    def _compute_display_name(self):
        """Computes the display name based on selected fields in 'Apply On'."""
        _ = self.env._
        fields_mapping = (
            (_("Category"), 'product_category_id'),
            (_("Product"), 'product_id'),
            (_("Salesperson"), 'user_id'),
            (_("Sales Team"), 'team_id')
        )
        for rule in self:
            conditions = [
                _("%(display_name)s: %(value)s", display_name=display_name, value=rule[fname].name)
                for display_name, fname in fields_mapping
                if rule[fname]
            ]
            if rule.max_discount:
                conditions.append(_("Max Discount: %s", rule.max_discount))
            if rule.product_expired:
                conditions.append(_("Product Expired: %s", rule.product_expired))
                
            rule.display_name = _(" AND ").join(conditions) if conditions else _("No Conditions")
