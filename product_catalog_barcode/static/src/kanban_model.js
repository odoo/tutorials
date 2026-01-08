/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { getScannedProducts } from "./scanned_products";


patch(ProductCatalogKanbanModel.prototype, {
    async _loadData(params) {
        const result = await super._loadData(...arguments);
        if (!params.isMonoRecord && !params.groupBy.length) {
            const scannedProducts = getScannedProducts();
            result.records.sort((a, b) => {
                const aIsScanned = scannedProducts.has(a.id);
                const bIsScanned = scannedProducts.has(b.id);
                return bIsScanned - aIsScanned; 
            });
        }
        return result;
    }
});
