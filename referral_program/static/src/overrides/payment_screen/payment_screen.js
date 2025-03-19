import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
    },
    //@override
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        const partner = order.get_partner()
        if(partner && partner.referred_by && order.get_total_paid()>0) {
	        const coupondata = {
                partner_id : partner.referred_by.id,
                points : order.get_total_paid() * 0.10,
                expiration_date : luxon.DateTime.now().plus({ month: 3 }),
            }
            await this.pos.data.call("pos.order", "generate_gift_card", [
                order.id,
                coupondata,
            ]);
        }
        await super.validateOrder(...arguments);
    },
});
