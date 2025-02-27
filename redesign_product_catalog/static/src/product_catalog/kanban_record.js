/** @odoo-module */

import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { patch } from "@web/core/utils/patch";

patch(ProductCatalogKanbanRecord.prototype, {
    onGlobalClick(ev) {
        if (ev.target.closest(".o_product_catalog_cancel_global_click")) {
            return;
        }

        if(this.env.isSmall && ev.target.closest(".o_product_image")) {
            return;
        }
        
        if (this.productCatalogData.quantity === 0) {
            this.addProduct();
        } else {
            this.increaseQuantity();
        }
    }
});
