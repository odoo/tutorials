from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    publish_date = fields.Date(readonly=True, copy=False)
    has_manual_ribbon = fields.Boolean(
        compute='_compute_has_manual_ribbon', copy=False, store=True
    )

    @api.depends('website_ribbon_id')
    def _compute_has_manual_ribbon(self):
        for product in self:
            if not product.website_ribbon_id:
                product.has_manual_ribbon = False

    def _set_ribbon(self, products_prices):
        self.ensure_one()
        product_ribbons = self.env['product.ribbon'].sudo()

        if self.has_manual_ribbon:
            return None

        def _add_ribbon(ribbon):
            if ribbon.id != self.website_ribbon_id.id:
                self.with_context(auto_assign_ribbon=True).write({
                    'website_ribbon_id': ribbon.id
                })

        stock_ribbon = product_ribbons.search([('assign', '=', 'out_of_stock')])
        if stock_ribbon and self._is_sold_out() and not self.allow_out_of_stock_order:
            return _add_ribbon(stock_ribbon[0])

        sale_ribbon = product_ribbons.search([('assign', '=', 'sale')])
        if sale_ribbon and (
            products_prices.get('price_reduce')
            < products_prices.get('base_price', self.list_price)
        ):
            return _add_ribbon(sale_ribbon[0])

        new_ribbon = product_ribbons.search([('assign', '=', 'new')])
        if new_ribbon and self.publish_date:
            if (fields.Date.today() - self.publish_date).days <= new_ribbon.new_until:
                return _add_ribbon(new_ribbon[0])

        return self.write({'website_ribbon_id': False})

    def write(self, vals):
        if 'website_ribbon_id' in vals:
            if self.env.context.get('auto_assign_ribbon'):
                vals['has_manual_ribbon'] = False
            else:
                vals['has_manual_ribbon'] = bool(vals['website_ribbon_id'])

        if 'is_published' in vals:
            # Set publish date when publishing
            if vals['is_published'] and not self.is_published:
                vals['publish_date'] = fields.Date.today()

            # Clear publish date when unpublishing
            elif not vals['is_published']:
                vals['publish_date'] = False

        return super().write(vals)
