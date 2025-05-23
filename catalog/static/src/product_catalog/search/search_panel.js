/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { ProductCatalogSearchPanel} from "@product/product_catalog/search/search_panel";
import { useState} from "@odoo/owl";
import { useBus } from "@web/core/utils/hooks"
import { bus } from "../bus"

patch(ProductCatalogSearchPanel.prototype, {
    setup() {
        super.setup()
        this.state = useState(this.getDefaultSelectionState());
        useBus(bus, 'TOGGLE_CHEK_BOX', this.toggleCheckBoxUsingCard)
    },

    toggleCheckBoxUsingCard(info) {
      if (!this.state.result[info.detail.category_id]) {
        this.state.result[info.detail.category_id] = !this.state.result[info.detail.category_id]
      }
    },

    getDefaultSelectionState() {
      const childIds = new Set(this.env.searchModel._context.child_ids);
      const result = {}
      this.sections[0].values.forEach((value, key) => {
        result[value.id] = childIds.has(value.id);
      });
      return {...this.state, result}
    },

    /** override **/
    async toggleSectionCategoryValue(filterId, attrIds, { currentTarget }) {
        this.state.result[filterId] = !this.state.result[filterId]
        const data = {
            catalog_id: this.env.searchModel._context.order_id,
            category_id: filterId,
            checkbox_checked: this.state.result[filterId],
            removed_product_ids: this.env.searchModel.globalContext.removed_product_ids
        }
        return await rpc("/catalog/product_configurator/update_catalog_line_info", data)
    }
})
