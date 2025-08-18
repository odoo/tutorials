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
        product_ribbons = self.env['product.ribbon'].sudo()

        stock_ribbon = product_ribbons.search([('assign', '=', 'out_of_stock')], limit=1)
        sale_ribbon = product_ribbons.search([('assign', '=', 'sale')], limit=1)
        new_ribbons = product_ribbons.search([('assign', '=', 'new')])

        if not (stock_ribbon or sale_ribbon or new_ribbons):
            return

        def _add_ribbon(product, ribbon_id):
            if ribbon_id != product.website_ribbon_id.id:
                product.with_context(auto_assign_ribbon=True).sudo().write({
                    'website_ribbon_id': ribbon_id
                })

        for prd in self:
            if not prd.is_published or prd.has_manual_ribbon:
                continue

            if stock_ribbon:
                if (not prd.allow_out_of_stock_order) and prd._is_sold_out():
                    _add_ribbon(prd, stock_ribbon.id)
                    continue

            if sale_ribbon:
                prices = products_prices.get(prd.id)
                if prices.get('price_reduce') < prices.get('base_price', prd.list_price):
                    _add_ribbon(prd, sale_ribbon.id)
                    continue

            if prd.publish_date:
                published_for = (fields.Date.today() - prd.publish_date).days
                new_ribbon = False
                for ribbon in new_ribbons:
                    if ribbon.new_until >= published_for:
                        new_ribbon = ribbon
                        break
                if new_ribbon:
                    _add_ribbon(prd, new_ribbon.id)
                    continue

            _add_ribbon(prd, False)

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
