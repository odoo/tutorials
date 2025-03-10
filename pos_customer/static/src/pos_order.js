/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    getCustomerDisplayData() {
        const temp = this.getSortedOrderlines().map((l) => ({
            ...l.getDisplayData(),
            isRefund: l.refunded_orderline_id ? true : false,
        }));

        return {
            ...super.getCustomerDisplayData(),
            
            partnerName: this.get_partner_name() ? this.get_partner_name() : "Guest",
            amount_per_guest: this.amountPerGuest(),
            refundLines: temp.filter((x) => x.isRefund),
            lines: temp.filter((x) => !x.isRefund),
        };
    },
});
