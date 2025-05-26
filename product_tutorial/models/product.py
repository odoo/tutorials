from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command


class Product(models.Model):
    _name = 'product'
    _description = "Storable Product"
    _sql_constraints = [
        ('positive_price', 'CHECK (price >= 0)', "The sales price must be positive.")
    ]
    _check_company_auto = True

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    is_published = fields.Boolean(string="Published")
    price = fields.Float(string="Sales Price", required=True, default=100)
    cost = fields.Float(string="Manufacturing Cost", company_dependent=True)
    margin = fields.Float(
        string="Profit Margin", compute='_compute_margin', inverse='_inverse_margin', store=True
    )
    is_profitable = fields.Boolean(
        string="Profitable", compute='_compute_is_profitable', search='_search_is_profitable'
    )
    sales_count = fields.Integer(string="Sales Count")
    category_id = fields.Many2one(
        string="Category",
        comodel_name='product.category',
        ondelete='restrict',
        required=True,
        default=lambda self: self.env.ref('product_tutorial.category_apparel'),
        check_company=True,
    )
    category_name = fields.Char(string="Category Name", related='category_id.name')
    breadcrumb = fields.Char(
        string="Breadcrumb",
        help="The path to the product. For example: 'Home Decor / Coffee table'",
        compute='_compute_breadcrumb',
    )
    supplier_ids = fields.Many2many(
        string="Suppliers",
        help="The suppliers offering the product for sale.",
        comodel_name='res.partner',
        relation='product_supplier_rel',
        column1='product_id',
        column2='partner_id',
    )
    company_id = fields.Many2one(string="Company", comodel_name='res.company')
    active = fields.Boolean(default=True)

    @api.depends('price', 'cost', 'company_id')
    @api.depends_context('company')
    def _compute_margin(self):
        for product in self:
            product.margin = product.price - product.with_company(product.company_id).cost

    def _inverse_margin(self):
        for product in self:
            # As the cost is fixed, the sales price is increased to match the desired margin.
            product.price = product.cost + product.margin

    @api.depends('margin')
    def _compute_is_profitable(self):
        for product in self:
            product.is_profitable = product.margin > 0

    def _search_is_profitable(self, operator, value):
        if (operator == '=' and value is True) or (operator == '!=' and value is False):
            return [('margin', '>', 0)]
        elif (operator == '=' and value is False) or (operator == '!=' and value is True):
            return [('margin', '<=', 0)]
        else:
            raise NotImplementedError()

    @api.depends('name', 'category_name')
    def _compute_breadcrumb(self):
        for product in self:
            product.breadcrumb = f"{product.category_name} / {product.name}"

    @api.constrains('price', 'category_id')
    def _check_price_is_higher_than_category_min_price(self):
        for product in self:
            if product.price < product.category_id.min_price:
                raise ValidationError(
                    _("The price must be higher than %s.", product.category_id.min_price)
                )

    @api.onchange('supplier_ids')
    def _onchange_supplier_ids_unpublish_if_no_suppliers(self):
        if not self.supplier_ids:
            self.is_published = False

    @api.onchange('price')
    def _onchange_price_warn_if_margin_is_negative(self):
        if self.margin < 0:
            return {
                'warning': {
                    'title': _("Warning"),
                    'message': _(
                        "The sales price was changed from %(before_price)s to %(new_price)s, which"
                        " would result in a negative margin. A sales price of minimum %(min_price)s"
                        " is recommended.",
                        before_price=self._origin.price, new_price=self.price, min_price=self.cost,
                    ),
                }
            }

    @api.onchange('category_id')
    def _onchange_category_id_block_if_existing_sales(self):
        # existing_sales = self.env['sales.order'].search([('product_id', '=', self._origin.id)])
        existing_sales = False
        if existing_sales:
            raise UserError(_(
                "You cannot change the category of a product that has already been sold; unpublish"
                " it instead."
            ))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if category_id := vals.get('category_id'):  # A category is specified in the values.
                category = self.env['product.category'].browse(category_id).exists()
                if category and not category.active:  # The category exists and is archived.
                    vals['active'] = False  # Create the product in the inactive state.
        return super().create(vals_list)

    def write(self, vals):
        if new_category_id := vals.get('category_id'):  # The category of the product is updated.
            new_category = self.env['product.category'].browse(new_category_id).exists()
            if new_category and not new_category.active:  # The category exists and is archived.
                vals['active'] = False  # Archive the product.

        res = super().write(vals)

        for product in self:
            if not product.active and vals.get('active') is False:  # The product has been archived.
                if not product.category_id.product_ids:  # All the category's products are archived.
                    # Archive the category in sudo mode to allow writing on the category.
                    product.category_id.sudo().active = False

        return res

    @api.model
    def _reassign_inactive_products(self):
        # Find inactive products and clear their suppliers.
        underperforming_products = self.search([('sales_count', '<', 10)])
        underperforming_products.write({
            'supplier_ids': [Command.clear()],  # Remove all suppliers.
        })

        # Find products without suppliers and assign the default supplier.
        products_without_suppliers = self.search([('supplier_ids', '=', False)])
        if products_without_suppliers:
            default_supplier = self.env.ref('product_tutorial.default_supplier')
            products_without_suppliers.write({
                'supplier_ids': [Command.set(default_supplier.ids)]  # Set the default supplier.
            })
