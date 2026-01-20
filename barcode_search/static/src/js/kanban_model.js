/** @odoo-module */

import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import {patch} from "@web/core/utils/patch";
import { getFieldsSpec } from "@web/model/relational_model/utils";
import { orderByToString } from "@web/search/utils/order_by";

patch(ProductCatalogKanbanModel.prototype, {
    async _loadData(params){
        // params.limit = Number.MAX_SAFE_INTEGER;
        const result = await this._loadUngroupedList1({
            ...params,
            context: {
                ...params.context,
                current_company_id: params.currentCompanyId,
            },
        });

        console.log("result",result)

        return super._loadData(params);
    },

    async _loadUngroupedList1(config) {
        const orderBy = config.orderBy.filter((o) => o.name !== "__count");
        const kwargs = {
            specification: getFieldsSpec(config.activeFields, config.fields, config.context),
            offset: config.offset,
            order: orderByToString(orderBy),
            limit: Number.MAX_SAFE_INTEGER,
            context: { bin_size: true, ...config.context },
            count_limit:
                config.countLimit !== Number.MAX_SAFE_INTEGER ? config.countLimit + 1 : undefined,
        };
        return this.orm.webSearchRead(config.resModel, config.domain, kwargs);
    }

})
