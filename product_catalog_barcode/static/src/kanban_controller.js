/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";
import { clearScannedProducts } from "./scanned_products";


patch(ProductCatalogKanbanController.prototype, {
    async backToQuotation() {
        clearScannedProducts();
        await super.backToQuotation();
    },
});
