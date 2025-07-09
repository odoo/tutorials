import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { getFieldsSpec } from "@web/model/relational_model/utils";
import { rpc } from "@web/core/network/rpc";

export class CustomProductCatalogKanbanModel extends ProductCatalogKanbanModel {
    async _loadUngroupedList(config) {
        const ProductIds = await this.orm.search(config.resModel, config.domain);
        if (!ProductIds.length) {
            return { records: [], length: 0 };
        }

        let orderLinesInfo = {};
        if (config.context.order_id && config.context.product_catalog_order_model) {
            orderLinesInfo = await rpc("/product/catalog/order_lines_info", {
                order_id: config.context.order_id,
                product_ids: ProductIds,
                res_model: config.context.product_catalog_order_model,
            });
            ProductIds.sort((a, b) => (orderLinesInfo[b].quantity || 0) - (orderLinesInfo[a].quantity || 0));
        }

        const catalogPage = ProductIds.slice(config.offset, config.offset + config.limit);

        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields, config.context),
        };

        const result = await this.orm.webSearchRead(config.resModel, [["id", "in", catalogPage]], kwargs);

        result.records.sort((a, b) => (orderLinesInfo[b.id].quantity || 0) - (orderLinesInfo[a.id].quantity || 0));
        return {
            length: ProductIds.length,
            records: result.records,
        };
    }
}
