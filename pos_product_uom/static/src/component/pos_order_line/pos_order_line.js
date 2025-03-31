/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    set_unit(unit) {
        if (!unit || this.product_id.uom_id === unit) {
            return;
        }
        this.product_id.uom_id = unit;
        this.setDirty(); 
    }    
});
