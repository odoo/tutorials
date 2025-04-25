/** @odoo-module **/

import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { getFieldsSpec } from "@web/model/relational_model/utils";
import { rpc } from "@web/core/network/rpc";


export class SortProductCatalogKanbanModel extends ProductCatalogKanbanModel {

    async _loadUngroupedList(config) {
        const offset = config.offset ?? 0;
        const limit = config.limit ?? 40;

        let sortedProductIds = [];
        if (config.context.order_id && config.context.product_catalog_order_model) {
            sortedProductIds = await rpc('/product/catalog/sorted_product_ids', {
                order_id: config.context.order_id,
                res_model: config.context.product_catalog_order_model,
            });
        } else {
            sortedProductIds = await this.orm.search(config.resModel, config.domain);
        }

        const paginatedProducts = sortedProductIds.slice(offset, offset + limit);
        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields, config.context),
        };

        const result = await this.orm.webSearchRead(
            config.resModel,
            [["id", "in", paginatedProducts]],
            kwargs
        );

        return {
            length: sortedProductIds.length,
            records: result.records,
        };
    }

    async _loadData(config) {
        const result = await super._loadData(config);

        if (!config.isMonoRecord && !config.groupBy.length) {
            result.records.sort((a, b) => {
                const aQty = a.productCatalogData?.quantity || 0;
                const bQty = b.productCatalogData?.quantity || 0;
                return bQty - aQty;
            });
        }
        return result;
    }
}
