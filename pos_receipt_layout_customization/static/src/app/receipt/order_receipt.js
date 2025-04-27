import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { markup } from "@odoo/owl";


patch(OrderReceipt, {
     template: "pos_receipt_layout_customization.CustomOrderReceipt_main"
});
patch(OrderReceipt.prototype, {
    setup(){
        this.pos = usePos();
        this.footer = markup(this.props.data.footer)
        this.header = markup(this.props.data.header)
        // const rendered = this.pos.config.receipt_rendered_template;
        // this.rendered_receipt_html = markup(rendered || "<p>No Receipt Template Set</p>");

        // const layoutData = this.pos.models.find(m => m.model === 'pos.receipt.layout');
        // const rendered = layoutData?.data?.[0]?.rendered_template;
            
        // this.rendered_receipt_html = markup(rendered || "<p>No Template Found</p>");
    },
    
    get orderQuantity() {
        return this.props.data.orderlines.reduce((acc, line) => acc + parseFloat(line.qty), 0);
    },

    get order() {
        return this.pos.get_order()
    }
});
