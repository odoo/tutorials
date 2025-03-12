/** @odoo-module **/

import { registry } from "@web/core/registry";

export const productDataLoadService = {
    dependencies: ["orm"],
    async start(env, { orm }) {
        console.log("📡 Catalog Data Loader Service started. Loading products...");

        try {
            window.productData = await orm.call("product.product", "search_read", [[], ["id", "name", "barcode"]]);
            console.log("✅ Product Data Loaded:", window.productData);
        } catch (error) {
            console.error("❌ Error loading catalog data:", error);
        }
    },
};

// Register the service
registry.category("services").add("product_data_loader", productDataLoadService);
