import { rpc } from "@web/core/network/rpc";
import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { getFieldsSpec } from "@web/model/relational_model/utils";

export class BarcodeProductCatalogKanbanModel extends ProductCatalogKanbanModel {
    async _loadUngroupedList(config) { 
        const allProducts = await this.orm.search(config.resModel, config.domain);

        if (!allProducts.length) {
            return { records: [], length: 0 };
        }

        let orderLines = {};
        const scanned = [], unscanned = [];

        if (config.context.order_id && config.context.product_catalog_order_model) {
            orderLines = await rpc("/product/catalog/order_lines_info", {
                order_id: config.context.order_id,
                product_ids: allProducts,
                res_model: config.context.product_catalog_order_model,
            });

            for (const id of allProducts) {
                const qty = (orderLines[id]?.quantity) || 0;
                if (qty > 0) scanned.push(id);
                else unscanned.push(id);
            }

            scanned.sort((a, b) =>
                (orderLines[b]?.quantity || 0) - (orderLines[a]?.quantity || 0)
            );
        } else {
            unscanned.push(...allProducts);
        }

        const sortedIds = [...scanned, ...unscanned];
        const paginatedIds = sortedIds.slice(config.offset, config.offset + config.limit);

        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields, config.context), //passed through webserach() in orm
        };

        const result = await this.orm.webSearchRead(config.resModel, [["id", "in", paginatedIds]], kwargs);

        result.records.sort((a, b) => {
            const qtyA = orderLines[a.id]?.quantity || 0;
            const qtyB = orderLines[b.id]?.quantity || 0;
            return qtyB - qtyA || a.id - b.id;
        });

        return {
            length: allProducts.length,
            records: result.records,
        };
    }
}
