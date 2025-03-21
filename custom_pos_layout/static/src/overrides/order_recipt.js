import { patch } from "@web/core/utils/patch";
import { useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

patch(OrderReceipt.prototype, {
    setup() {
        super.setup(...arguments);
        console.log("PROPSSS ")
        console.log("from order_recipt");
        this.state = useState({
            disp_layout: "default", // Default layout
        });
        
        onWillStart(async ()=>{
            const result = await rpc("/pos/get_display_layout", {});
            console.log("THE OBJECT OF RPC IS ",result);
            if (result && result.disp_layout) {
                this.state.disp_layout = result.disp_layout;
            }
        })

        this.receipt = this.props.data; // Access receipt data from props
        let totalQty = 0;
        if (this.receipt && this.receipt.orderlines) {
            this.receipt.orderlines.forEach(line => {
                totalQty += parseFloat(line.qty);
            });
            this.receipt.totalQty = totalQty; // Add totalQty to receipt data
        }
        console.log("TAX TOTALS");
        console.log(this.props.data.taxTotals.subtotals);
    },
});
