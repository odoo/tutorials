/** @odoo-module **/

import { formatCurrency } from '@web/core/currency';
import { patch } from '@web/core/utils/patch';
import { Product } from '@sale/js/product/product';

patch(Product.prototype, {
    getFormattedPrice(...subtotal) {
        if (subtotal.length != 0) {
            return formatCurrency(subtotal[0], this.env.currency.id);
        }
        return super.getFormattedPrice();
    }
});
