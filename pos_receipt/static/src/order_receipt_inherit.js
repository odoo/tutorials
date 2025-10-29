import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(OrderReceipt, {
    template: "pos_receipt.order_receipt_inherited"
});

patch(OrderReceipt.prototype, {
    setup(){
        super.setup();
        this.pos = usePos();
    },

    get orderQuantity() {
        return this.props.data.orderlines.reduce((acc, line) => acc + parseFloat(line.qty), 0);
    },

    get order() {
        return this.pos.get_order();
    }
});
