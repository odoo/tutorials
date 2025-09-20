import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    getCustomerDisplayData() {
        const orderlines = this.getSortedOrderlines();

        const activeItems = [];
        const refundedItems = [];
        for (const line of orderlines) {
            if (line.refunded_orderline_id) {
                refundedItems.push(line.getDisplayData());
            } else {
                activeItems.push(line.getDisplayData());
            }
        }

        const guests = Math.max(this.guest_count || 0, 0);
        const totalWithTax = this.get_total_with_tax();
        const amountPerGuest = guests > 0 ? totalWithTax / guests : null;

        return {
            ...super.getCustomerDisplayData(),

            customerName: this.get_partner_name() || "Guest",
            amountPerGuest,
            activeItems,
            refundedItems,
        };
    },
});
