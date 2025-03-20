import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { patch } from "@web/core/utils/patch";

patch(ProductCatalogKanbanModel.prototype, {
    async _loadData(params) {
        const result = await super._loadData(...arguments);

        console.log("Before Reset & Sorting:", result.records.map(r => ({
            id: r.id,
            last_invoice_time_diff: r.last_invoice_time_diff
        })));

        const sortedRecords = [...result.records];

        sortedRecords.sort((a, b) => {
            const timeA = a.last_invoice_time_diff || ""; 
            const timeB = b.last_invoice_time_diff || "";
            return timeB.localeCompare(timeA); 
        });

        console.log("After Reset & Sorting:", sortedRecords.map(r => ({
            id: r.id,
            last_invoice_time_diff: r.last_invoice_time_diff
        })));

        return { ...result, records: sortedRecords };
    }
});
