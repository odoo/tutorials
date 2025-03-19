/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { bus } from "./bus"

patch(ProductCatalogKanbanRecord.prototype, {
    setup() {
      super.setup()
      this.state = useState({removed_product_ids:this.env.searchModel.globalContext.removed_product_ids})
    },

    /** override **/
    async onGlobalClick(ev) {
        let is_add;
        if (this.env.orderResModel == 'catalog.catalog') {
            const product_id = this.env.productId
            const index = this.state.removed_product_ids.indexOf(product_id)
            if (index !== -1) {
                is_add = true
                this.state.removed_product_ids.splice(index, 1)
            } else {
                is_add = false
                this.state.removed_product_ids.push(product_id)
                bus.trigger('TOGGLE_CHEK_BOX', {category_id: this.props.record.productCatalogData.product_categ_id})
            }
            const data = {
                'catalog_id': this.props.record.evalContext.context.active_id,
                'category_id': this.props.record.productCatalogData.product_categ_id,
                'product_id': this.props.record.data.id,
                'is_add': is_add
            }
            return await rpc("/catalog/product_configurator/update_catalog_line_info/using_record", data)
        }
        return super.onGlobalClick(ev)
    }
})
