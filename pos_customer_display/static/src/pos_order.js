import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";


patch(PosOrder.prototype, {
    getCustomerDisplayData() {
        const orderLines = [];
        const refundLines = [];
        this.getSortedOrderlines().forEach((line) => {
            const linesData = {
                ...line.getDisplayData(),
                isSelected: line.isSelected(),
                imageSrc: `/web/image/product.product/${line.product_id.id}/image_128`,
            };
            if (line.refunded_orderline_id) {
                refundLines.push(linesData);
            } else {
                orderLines.push(linesData);
            }
        });

        return {
            ...super.getCustomerDisplayData(),
            partner: this.partner_id ? {name: this.partner_id.name,}: null,
            amountperguest: this.amountPerGuest(),
            orderLines: orderLines,
            refundLines: refundLines,
        };
    },
});
