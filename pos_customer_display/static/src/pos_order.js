import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";


patch(PosOrder.prototype, {
    getCustomerDisplayData(){
        const allOrderLines = this.getSortedOrderlines();
        const refundOrderLines = allOrderLines.filter((rl) => rl.refunded_orderline_id);
        const nonRefundOrderLines = allOrderLines.filter((nrl) => !nrl.refunded_orderline_id);
        const customerCount = this.customer_count || 0;

        return{
            ...super.getCustomerDisplayData(),
            customerName: this.get_partner_name() ?? "",
            amountPerGuest: this.amountPerGuest(customerCount),
            refundOrderLines: refundOrderLines.map((x) => x.getDisplayData()),
            orderLines: nonRefundOrderLines.map((x) => x.getDisplayData()),
        }
    }
});
