import { patch } from "@web/core/utils/patch";
import { getFieldsSpec } from "@web/model/relational_model/utils";

import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";

patch(ProductCatalogKanbanModel.prototype, {

    /**
     * Overrides "_loadUngroupedList" to fetch all products and sort them 
     * based on their quantity in the current order.
     *
     * @returns {Object} - Paginated product list sorted by quantity in the order.
     */
    async _loadUngroupedList(config) {
        const orderId = config.context.order_id;
        const orderResModel = config.context.product_catalog_order_model;
        const activeModel = config.context.active_model;

        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields),
            context: { bin_size: true, ...config.context },
        };

        const allProducts = await this.orm.webSearchRead(config.resModel, config.domain, kwargs);

        const productQuantity = await this.fetchOrderQuantities(orderId, activeModel, orderResModel);

        allProducts.records.sort((a, b) => {
            return (productQuantity[b.id] ?? 0) - (productQuantity[a.id] ?? 0);
        });

        const { offset = 0, limit } = config;
    
        return {
            records: allProducts.records.slice(offset, offset + limit),
            length: allProducts.records.length,
        };
    },

    /**
     * Fetches the product quantities from order lines based on the order type (Sale/Purchase).
     *
     * @param {number} orderId - The ID of the current order.
     * @param {string} activeModel - The model name of the order lines.
     * @param {string} orderResModel - The model name of the order (sale.order or purchase.order).
     * @returns {Object} - A dictionary mapping product IDs to their quantity in the order.
     */
    async fetchOrderQuantities(orderId, activeModel, orderResModel) {
        if(!orderId) return {}

        let orderLineQty = orderResModel == "sale.order" ? "product_uom_qty" : "product_qty";

        const orderLines = await this.orm.searchRead(
            activeModel,
            [["order_id", "=", orderId]],
            ["product_id", orderLineQty]
        );
        
        const result = orderLines.reduce((acc, line) => {
            acc[line.product_id[0]] = line[orderLineQty];
            return acc;
        }, {});

        return result;
    },
});
