/** @odoo-module **/

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    showScreen(payment=false, receipt=false) {
        this.showPaymentScreen = payment;
        this.showReceiptScreen = receipt;
    },
});
