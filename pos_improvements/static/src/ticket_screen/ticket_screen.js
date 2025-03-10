import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";

patch(TicketScreen.prototype, {
    customPayment() {
        const selectedOrder = this.state.selectedOrder;

        if (!selectedOrder) {
            console.error("No selected order found!");
            return;
        }
        this.pos.set_order(selectedOrder);
        this.pos.pay()
    },
});
