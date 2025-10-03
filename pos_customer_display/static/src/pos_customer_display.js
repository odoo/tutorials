import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        this.guest_count = this.guest_count || 1;
    },

    getGuestCount() {
        return this.guest_count || 1;
    },

    getCustomerDisplayData() {
        const allOrderlines = this.getSortedOrderlines();
        const refundedOrderLines = allOrderlines.filter((order) => order.refunded_orderline_id);
        const nonRefundOrderLines = allOrderlines.filter((order) => !order.refunded_orderline_id);
        const guestCount = this.getGuestCount();
        const amountPerGuest = this.get_total_with_tax() / guestCount;

        return {
            ...super.getCustomerDisplayData(),
            customerName: this.get_partner_name() ? this.get_partner_name() : "Guest",
            isRefundOrder: this._isRefundOrder(),
            refundedOrderLines: refundedOrderLines.map((x) => x.getDisplayData()),
            orderLines: nonRefundOrderLines.map((x) => x.getDisplayData()),
            amountPerGuest: amountPerGuest,
        };
    },
});
