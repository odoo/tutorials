import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { markup } from "@odoo/owl";

patch(OrderReceipt, {
    template: "pos_receipt_customize.order_view_inherited"
});

patch(OrderReceipt.prototype, {
    setup() {
        this.pos = usePos();
        this.footer = markup(this.props.data.receipt_footer_html || "");
    },

    get orderQuantity() {
        return this.props.data.orderlines.reduce((accumulator, line) => accumulator + parseFloat(line.qty), 0);
    },

    get order() {
        return this.pos.get_order()
    }
});
