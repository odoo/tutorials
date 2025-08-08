import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    getCustomerDisplayData() {
        const allLines = this.getSortedOrderlines();
        const returnedItems = allLines.filter(line => line.refunded_orderline_id);
        const saleItems = allLines.filter(line => !line.refunded_orderline_id);

        const guests = this.guest_count || 0;
        const total = this.get_total_with_tax();
        const perGuestAmount = guests > 0 ? total / guests : null;

        return {
            ...super.getCustomerDisplayData(),

            displayCustomerName: this.get_partner_name() || "Guest",
            amountDividedPerGuest: perGuestAmount,
            refundedItems: returnedItems.map(line => line.getDisplayData()),
            activeItems: saleItems.map(line => line.getDisplayData()),
        };
    },
});
