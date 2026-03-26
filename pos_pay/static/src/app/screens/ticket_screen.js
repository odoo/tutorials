import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";

patch(TicketScreen.prototype, {
    payFromTicketScreen() {
        const selectedOrder = this.getSelectedOrder();
        if (!selectedOrder) {
            this.env.services.notification.add("No order selected");
            return;
        }
        this.setOrder(selectedOrder);
        this.pos.pay();
    },
});
