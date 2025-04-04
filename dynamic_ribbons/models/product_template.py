from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_ribbon_auto = fields.Boolean("Automatic Ribbon", default=False)

    def _get_ribbon(self, products_prices):
        self.ensure_one()

        product_ribbon_sudo = self.env['product.ribbon'].sudo()

        if self.website_ribbon_id and not self.website_ribbon_auto:
            return

        # if (True):
        #     continue

        # Out of Stock Ribbon
        out_of_stock_ribbon = product_ribbon_sudo.search([('assign', '=', 'out_of_stock')])
        if out_of_stock_ribbon and self.qty_available <= 0.0 and not self.allow_out_of_stock_order:
            self.website_ribbon_id = out_of_stock_ribbon.id
            self.website_ribbon_auto = True
            return 

        # Sale Ribbon
        pricelist_price = products_prices[self.id].get('price_reduce')
        sale_ribbon = product_ribbon_sudo.search([('assign', '=', 'sale')])
        if sale_ribbon and (pricelist_price < self.list_price or self.list_price < self.compare_list_price):            
            self.website_ribbon_id = sale_ribbon.id
            self.website_ribbon_auto = True
            return

        # New Product Ribbon
        new_ribbon = product_ribbon_sudo.search([('assign', '=', 'new')])
        if new_ribbon:
            days_since_publish = (fields.Date.today() - self.create_date.date()).days
            if days_since_publish <= new_ribbon.show_period:
                self.website_ribbon_id = new_ribbon.id
                self.website_ribbon_auto = True
                return  

        # If no ribbon was assigned automatically then clearing any existing automatic ribbon
        self.website_ribbon_id = None


    def write(self, vals):
        if 'website_ribbon_id' in vals and vals['website_ribbon_id'] != self.website_ribbon_id.id:
            vals['website_ribbon_auto'] = False
        return super().write(vals)
