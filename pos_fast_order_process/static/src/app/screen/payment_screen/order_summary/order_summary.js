/** @odoo-module **/

import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { patch } from "@web/core/utils/patch";

patch(OrderSummary.prototype, {
    clickLine(ev, orderline) {
        if (this.pos.config.pos_fast_order_process && !this.env.isSmall){
            if (
                this.numberBuffer?._currentBufferHolder?.component?.constructor?.name !== 'OrderSummary'
            ) {
                this.numberBuffer?.switchComponentStack("OrderSummary");
            } else {
                this.numberBuffer?.reset();
            }
        };
        super.clickLine(ev, orderline);
    },
});
