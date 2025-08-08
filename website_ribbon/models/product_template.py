from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ribbon_auto = fields.Boolean(default=False)

    def _assign_ribbon(self, ribbon):
        """Assign the given ribbon and mark it as auto-assigned."""
        self.website_ribbon_id = ribbon.id
        self.ribbon_auto = True

    def _get_ribbon(self, products_prices):
        self.ensure_one()

        # If already has manual ribbon, do nothing
        if self.website_ribbon_id and not self.ribbon_auto:
            return

        ribbon_model = self.env['product.ribbon'].sudo()

        # Get all ribbons sorted by sequence
        ribbons = ribbon_model.search([], order="sequence asc")

        # Loop through the ribbons and assign the first matching one
        for ribbon in ribbons:
            if ribbon.assign == 'out_of_stock':
                # Handle out-of-stock ribbon
                if self.qty_available <= 0.0 and not self.allow_out_of_stock_order:
                    return self._assign_ribbon(ribbon)

            elif ribbon.assign == 'sale':
                # Handle sale ribbon
                pricelist_price = products_prices[self.id].get('price_reduce')
                if pricelist_price < self.list_price or self.list_price < self.compare_list_price:
                    return self._assign_ribbon(ribbon)

            elif ribbon.assign == 'new':
                # Handle new ribbon
                new_ribbon = ribbon
                create_date = self.create_date.date() if self.create_date else None
                if create_date:
                    days_since_create = (fields.Date.today() - create_date).days
                    if days_since_create <= new_ribbon.days:
                        return self._assign_ribbon(new_ribbon)

        # Clear ribbon if no match
        self.website_ribbon_id = None
        self.ribbon_auto = False

    def write(self, vals):
        # If user manually changes the ribbon, disable auto
        if 'website_ribbon_id' in vals and vals['website_ribbon_id'] != self.website_ribbon_id.id:
            vals['ribbon_auto'] = False
        return super().write(vals)
