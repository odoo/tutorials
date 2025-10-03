import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@pos_self_order/app/components/product_card/product_card";
import { ProductPage } from "@pos_self_order/app/pages/product_page/product_page";
import { markup } from "@odoo/owl";

// Patch ProductCard to always navigate to the product page on selection,
// enabling display of self_order_description and large image for all products.
patch(ProductCard.prototype, {
    async selectProduct(qty = 1) {
        const product = this.props.product;

        if (!product.self_order_available || !this.isAvailable) {
            return;
        }

        // For combo products, we use the default behavior
        if (product.isCombo()) {
            return super.selectProduct(qty);
        }
        
        // For other products, navigate to the product page
        this.router.navigate("product", { id: product.id });
    }
});

// Patch ProductPage component to fetch and display self_order_description
patch(ProductPage.prototype, {
    async setup() {
        // call the original setup method to ensure the component is initialized properly
        super.setup();

        // This ensures that the product's self_order_description is fetched
        const product = this.props.product;
        if (product && !product.self_order_description) {
            try {
                const orm = this.env.services.orm;
                // orm.read() returns all fields of product.product, including those added by other modules via _inherit = "product.product".
                const [record] = await orm.read("product.product",[product.id]);
                if (record && record.self_order_description) {
                    // markup is used to safely render HTML content
                    product.self_order_description = markup(record.self_order_description);
                }
            } catch (err) {
                console.error("Failed to fetch self_order_description via ORM:", err);
            }
        }
    },
});
