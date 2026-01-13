import { patch } from "@web/core/utils/patch";
import { CustomerDisplayPosAdapter } from "@point_of_sale/app/customer_display/customer_display_adapter";

patch(CustomerDisplayPosAdapter.prototype, {
    getCurrencySymbol(order) {
        return order.currency?.symbol || "";
    },

    formatOrderData(order) {
        super.formatOrderData(order);
        this.data.partner_id = order.getPartnerName();
        this.data.amountPerGuest = order.amountPerGuest();
        this.data.is_refund = order.is_refund;
        this.data.currency_symbol = this.getCurrencySymbol(order);
    },
});
