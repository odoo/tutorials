import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { getFieldsSpec } from "@web/model/relational_model/utils";
import { orderByToString } from "@web/search/utils/order_by";

export class CustomProductCatalogKanbanModel extends ProductCatalogKanbanModel {
    async _loadUngroupedList(config) {
        const orderBy = config.orderBy.filter((o) => o.name !== "__count");
        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields, config.context),
            offset: config.offset,
            order: orderByToString(orderBy),
            limit: config.limit,
            context: { bin_size: true, ...config.context },
            count_limit: config.countLimit !== Number.MAX_SAFE_INTEGER ? config.countLimit + 1 : undefined,
        };

        if (config.context.product_catalog_order_model && config.context.order_id) {
            const orderId = config.context.order_id;
            
            const addedProductIds = await this.orm.searchRead(
                config.context.active_model,
                [["order_id", "=", orderId], ["product_id", "!=", false]],
                ["product_id"],
                { context: config.context }
            ).then(lines => [...new Set(lines.map(line => line.product_id?.[0]))]);

            const newDomain = [...config.domain, ["id", "in", addedProductIds]];
            return this.orm.webSearchRead(config.resModel, newDomain, kwargs);
        }
        return super._loadUngroupedList(config);
    }
}
