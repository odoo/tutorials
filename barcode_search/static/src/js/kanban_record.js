/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";  // Ensure correct import

const activeKanbanRecords = new Map(); // Store active Kanban records

patch(ProductCatalogKanbanRecord.prototype, {
    setup() {
        super.setup();

        const productId = this.props.record.resId;
        if (productId) {
            activeKanbanRecords.set(productId, this);
            console.log(`📝 Kanban Record Registered: Product ID ${productId}`);
        } else {
            console.warn("⚠️ Could not register Kanban Record. Missing product ID.");
        }
        // console.log(this.props.record.productCatalogData);
    },

    addProductFromBarcode(qty = 1) {
        console.log(`🔼 Increasing Quantity for Product ID ${this.env.productId}`);
        this.addProduct(qty);
    },

});

export { activeKanbanRecords };
