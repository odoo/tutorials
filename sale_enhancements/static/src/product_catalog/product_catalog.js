import { patch } from "@web/core/utils/patch";
import { ProductCatalogOrderLine } from "@product/product_catalog/order_line/order_line";
import { formatMonetary } from "@web/views/fields/formatters";
import { onMounted } from "@odoo/owl";

patch(ProductCatalogOrderLine.prototype, {
    setup() {
        onMounted(() => {
            const priceElement = document.querySelector(`#product-${this.props.productId}-price span.o_product_catalog_price`);
            if (priceElement) {
                priceElement.textContent = this.price;
            }
        });
    },
    get price() {
        const { currencyId, digits } = this.env;
        const formatPrice = formatMonetary(this.props.price, { currencyId, digits });
        return `${formatPrice}/Units`;
    }
});
