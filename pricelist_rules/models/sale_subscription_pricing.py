# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleSubscriptionPricing(models.Model):
    _name = 'sale.subscription.pricing'
    _inherit = ['sale.subscription.pricing', 'product.pricelist.item']

    compute_price = fields.Selection(
        selection=[
            ('percentage', "Discount"),
            ('formula', "Formula"),
            ('fixed', "Fixed Price"),
        ],
        help="Use the discount rules and activate the discount settings in order to show discount to customer.",
        index=True, default='percentage', required=True) 

    @api.model_create_multi
    def create(self, vals_list):
        records = self.env[self._name]
        Product = self.env['product.product']
        Category = self.env['product.category']  

        for vals in vals_list:
            vals_copy = vals.copy()
            display_on = vals.get('display_applied_on')
            categ_id = vals.get('categ_id')
            product_tmpl_id = vals.get('product_tmpl_id')

            domain = [('recurring_invoice', '=', True)]  

            if display_on == '2_product_category' and categ_id:
                category = Category.browse(categ_id)
                if not category.exists():  
                    raise UserError("Selected category does not exist.")
                domain.append(('categ_id', '=', category.id))
            elif display_on == '1_product' and product_tmpl_id:
                domain.append(('product_tmpl_id', '=', product_tmpl_id))
            else:
                raise UserError("You cannot create a subscription-based rule for a non-subscribable category.")

            products = Product.search(domain, limit=None if display_on == '2_product_category' else 1)

            if not products:
                raise UserError("No subscribable products found for the selected criteria.")

            for product in products:
                if self.env['sale.subscription.pricing'].search_count([
                    ('product_id', '=', product.id),
                    ('plan_id', '=', vals.get('plan_id')),
                    ('pricelist_id', '=', vals.get('pricelist_id')),
                ]) > 0:
                    raise UserError("A pricing already exists for this product, plan, and pricelist.")

                vals_copy.update({
                    'product_id': product.id,
                    'product_template_id': product.product_tmpl_id.id,
                    'product_tmpl_id': product.product_tmpl_id.id
                })
                records += super().create([vals_copy])
        return records

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        self.product_tmpl_id = self.product_template_id
