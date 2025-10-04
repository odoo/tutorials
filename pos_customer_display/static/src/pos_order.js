/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    getCustomerDisplayData() {
        const lines = this.getSortedOrderlines();
        const refundLines = lines.filter((l) => l.refunded_orderline_id);
        const nonRefundLines = lines.filter((l) => !l.refunded_orderline_id);

        return {
            ...super.getCustomerDisplayData(),

            partnerName: this.get_partner_name() ? this.get_partner_name() : "Guest",
            amount_per_guest: this.amountPerGuest,
            refundLines: refundLines.map((l) => l.getDisplayData()),
            lines: nonRefundLines.map((l) => l.getDisplayData()),
        };
    },
});
