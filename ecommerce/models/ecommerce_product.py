from odoo import fields, models,api


class EcommerceProduct(models.Model):
    _name = 'ecommerce.product'
    _description = 'E-commerce Product'

    title = fields.Char('title', required=True, help="Title of the product")
    description = fields.Text('Description', help="Description of the product")
    price = fields.Float('Price', required=True, help="Price of the product", default=0.0)
    quantity = fields.Integer('Quantity', required=True, help="Available quantity of the product", default=0)
    category_id = fields.Many2one(
        comodel_name='ecommerce.product.category',
        string='Category',
        help="Category of the product",
    )
    available = fields.Boolean(
        string='Available',
        compute='_compute_is_available',
        store=True,
        help="Indicates if the product is valid",
        default=False,)






    @api.depends('available', 'quantity')
    def _compute_is_available(self):
        for product in self:
            if product.quantity > 0 :
                product.available = True

    
