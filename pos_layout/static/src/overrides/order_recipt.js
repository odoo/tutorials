import { patch } from "@web/core/utils/patch";
import { useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

patch(OrderReceipt.prototype, {
    setup() {
        super.setup(...arguments);
        this.state = useState({
            disp_layout: "default",
        });

        onWillStart(async ()=>{
            const result = await rpc("/pos/get_display_layout", {});
            if (result && result.disp_layout) {
                this.state.disp_layout = result.disp_layout;
            }
        })

        this.receipt = this.props.data;
        let totalQty = 0;
        if (this.receipt && this.receipt.orderlines) {
            this.receipt.orderlines.forEach(line => {
                totalQty += parseFloat(line.qty);
            });
            this.receipt.totalQty = totalQty;
        }
    },
});
