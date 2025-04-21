/** @odoo-module **/

import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";


export class SortProductCatalogKanbanModel extends ProductCatalogKanbanModel {
    async _loadData(params) {
        const result = await super._loadData(...arguments);

        if (!params.isMonoRecord && !params.groupBy.length) {
            result.records.sort((a, b) => {
                const aQty = a.productCatalogData?.quantity || 0;
                const bQty = b.productCatalogData?.quantity || 0;
                return bQty - aQty; 
            });
        }

        return result;
    }
}
