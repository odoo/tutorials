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
            
            const [addedProductIds, totalAll] = await Promise.all([
                this.orm.searchRead(
                    config.context.active_model,
                    [['order_id', '=', orderId], ['product_id', '!=', false]],
                    ['product_id'],
                    { context: config.context }
                ).then(lines => [...new Set(lines.map(line => line.product_id?.[0]))]),
                this.orm.searchCount(config.resModel, config.domain)
            ]);

            if (addedProductIds.length > 0) {
                const totalAdded = addedProductIds.length;
                const start = config.offset;
                const remainingLimit = Math.max(0, config.limit - Math.max(0, totalAdded - start));
                const remainingOffset = Math.max(0, start - totalAdded);
                
                const [addedRecords, remainingRecords] = await Promise.all([
                    start < totalAdded ? this.orm.webSearchRead(
                        config.resModel,
                        [...config.domain, ['id', 'in', addedProductIds]],
                        { ...kwargs, offset: start, limit: config.limit }
                    ).catch(() => ({ records: [], length: 0 })) : { records: [], length: 0 },
                    
                    remainingLimit > 0 ? this.orm.webSearchRead(
                        config.resModel,
                        [...config.domain, ['id', 'not in', addedProductIds]],
                        { ...kwargs, offset: remainingOffset, limit: remainingLimit }
                    ).catch(() => ({ records: [], length: 0 })) : { records: [], length: 0 }
                ]);

                return {
                    records: [...(addedRecords.records || []), ...(remainingRecords.records || [])],
                    length: totalAll
                };
            }
        }
        return super._loadUngroupedList(config);
    }
}
