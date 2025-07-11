import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(OrderReceipt, {
  template: "pos_receipt.order_receipt_inherited",
});
patch(OrderReceipt.prototype, {
  setup() {
    super.setup();
    this.pos = usePos();
  },

  get order() {
    return this.pos.get_order();
  },

  get orderQuntity() {
    return this.props.order.orderlines.reduce(
      (sum, line) => sum + line.quantity,
      0
    );
  },
});
