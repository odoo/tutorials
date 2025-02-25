/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";

patch(ReceiptScreen.prototype, {
    orderDone() {
        if(this.pos.config.pos_fast_order_process){
            this.currentOrder.showScreen();
            this.pos.get_order().partner_id = null;
        };
        super.orderDone();
    },
});
