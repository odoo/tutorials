import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(OrderReceipt, {
    props: {
        ...OrderReceipt.props,
        simplified_receipt: { type: Boolean, optional: true },
    },

    defaultProps: {
        ...OrderReceipt.defaultProps,
        simplified_receipt: true,
    }
});

patch(OrderReceipt.prototype, {
    setup() {
        super.setup()
        this.pos = usePos()
        this.guestLines()
    },

    guestLines() {
        let customerCount = this.pos.get_order().getCustomerCount();
        let totalAmount = parseFloat(this.props.data.total_paid)
        let items = []
        for (let i = 0; i < customerCount; i++) {
            items.push({ id: i, name: `Menuitem ${i + 1}`, price: (totalAmount / customerCount).toFixed(2)});
        }
        this.guests = items
    }
})
