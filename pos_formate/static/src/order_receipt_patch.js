import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { ReceiptHeader } from "@point_of_sale/app/screens/receipt_screen/receipt/receipt_header";

patch(ReceiptHeader.prototype, {
  get props() {
    return {
      ...super.props,
      data: {
        ...this.props.data,
        company_logo: this.props.data.company?.company_logo,
      },
    };
  },
});

patch(OrderReceipt.prototype, {
  setup() {
    super.setup();
    this.pos = usePos();
  },

  template: "pos_formate.order_receipt_patch",

  get props() {
    const { receipt_header, receipt_footer, company_logo, receipt_layout } =
      this.pos.config;
    return {
      ...super.props,
      orderQuantity: this.orderQuantity,
      order: this.order,
      data: {
        ...this.props.data,
        header: receipt_header || this.props.data.header,
        footer: receipt_footer || this.props.data.footer,
        company_logo,
        layout: receipt_layout || "boxed",
      },
    };
  },

  get orderQuantity() {
    return this.props.data.orderlines.reduce(
      (sum, l) => sum + parseFloat(l.qty),
      0
    );
  },

  get order() {
    return this.pos.get_order();
  },
});
