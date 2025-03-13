import { patch } from "@web/core/utils/patch";
import { RelationalModel } from "@web/model/relational_model/relational_model";
import { getFieldsSpec } from "@web/model/relational_model/utils";
import { orderByToString } from "@web/search/utils/order_by";


patch(RelationalModel.prototype ,{
    async _loadUngroupedList(config) {
        const orderBy = config.orderBy.filter((o) => o.name !== "__count");
        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields, config.context),
            offset: config.offset,
            order: orderByToString(orderBy),
            limit: config.limit,
            context: { bin_size: true, ...config.context },
            count_limit:
                config.countLimit !== Number.MAX_SAFE_INTEGER ? config.countLimit + 1 : undefined,
        };

        if (config.resModel === 'product.product' && config.context.order_id) {
            const orderId = config.context.order_id;
    
            const addedProductIds = await this.orm.searchRead(
                config.context.active_model,
                [['order_id', '=', orderId], ['product_id', '!=', false]],
                ['product_id'],
                { context: config.context }
            ).then(lines => lines.map(line => line.product_id[0]));
            
            if (addedProductIds.length > 0) {
                const addedDomain = [...config.domain, ['id', 'in', addedProductIds]];
                const remainingDomain = [...config.domain, ['id', 'not in', addedProductIds]];
    
                const totalAdded = await this.orm.searchCount(config.resModel, addedDomain, { context: config.context });
                const totalRemaining = await this.orm.searchCount(config.resModel, remainingDomain, { context: config.context });
                const totalRecords = totalAdded + totalRemaining;
    
                const start = config.offset;
                const end = start + config.limit;
                let addedRecords = { records: [], length: 0 };
                let remainingRecords = { records: [], length: 0 };
    
                if (start < totalAdded) {
                    const addedLimit = Math.min(config.limit, totalAdded - start);
                    addedRecords = await this.orm.webSearchRead(
                        config.resModel,
                        addedDomain,
                        { ...kwargs, offset: start, limit: addedLimit }
                    ).catch(() => ({ records: [], length: 0 }));
                }
    
                if (end > totalAdded) {
                    const remainingOffset = Math.max(0, start - totalAdded);
                    const remainingLimit = config.limit - (addedRecords.records.length || 0);
                    remainingRecords = await this.orm.webSearchRead(
                        config.resModel,
                        remainingDomain,
                        { ...kwargs, offset: remainingOffset, limit: remainingLimit }
                    ).catch(() => ({ records: [], length: 0 }));
                }
    
                console.log("Added:", addedRecords.records.length, "Remaining:", remainingRecords.records.length, "Total:", totalRecords);
    
                return {
                    records: [
                        ...(addedRecords.records || []),
                        ...(remainingRecords.records || [])
                    ],
                    length: totalRecords 
                };
            }
        }

        return this.orm.webSearchRead(config.resModel, config.domain, kwargs);
    }
});

