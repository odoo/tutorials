import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { patch } from "@web/core/utils/patch";

patch(ProductCatalogKanbanModel.prototype, {
    async _loadData(params){
        const result = await super._loadData(...arguments);
        result.records.sort((a, b) => new Date(b.last_order_time) - new Date(a.last_order_time));
        return result;
    }
});
