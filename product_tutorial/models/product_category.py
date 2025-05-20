from odoo import fields, models


class ProductCategory(models.Model):
    _name = 'product.category'
    _description = "Product Category"
    _sql_constraints = [
        ('unique_name', 'unique(name)', "A category name must be unique.")
    ]
    _check_company_auto = True

    name = fields.Char(string="Name", required=True)
    min_price = fields.Float(string="Minimum Sales Price", required=True)
    product_ids = fields.One2many(
        string="Products", comodel_name='product', inverse_name='category_id', check_company=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.company.id,
    )
    active = fields.Boolean(default=True)

    def write(self, vals):
        for category in self:
            if category.active and vals.get('active') is False:  # The category is being archived.
                category.product_ids.active = False  # Archive all products of the category.
        return super().write(vals)

    def action_ensure_positive_margins(self):
        self.product_ids.filtered(lambda p: p.margin <= 0).margin = 0
        return True
