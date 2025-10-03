import { TicketScreen } from '@point_of_sale/app/screens/ticket_screen/ticket_screen';
import { patch } from '@web/core/utils/patch';

patch(TicketScreen.prototype, {
    async onPayClick() {
        this.pos.set_order(this.getSelectedOrder());
        this.pos.pay();
    },
});
