/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    add_new_order(data = {}) {
        if (this.config.pos_fast_order_process && !this.env.isSmall) {
            if(this.get_order()?.state !== 'draft' && this.get_order()?.showReceiptScreen){
                return this.get_order();
            }
            else if (this.get_order()?.get_partner() != null) {
                return this.get_order();
            };
        };
        this.get_order()?.showScreen();
        return super.add_new_order(data);
    },
    showScreen(name, props) {
        const temp = name;
        if (this.config.pos_fast_order_process && !this.env.isSmall) {
            if (name === "PaymentScreen" && props.orderUuid) {
                if (props?.others) {
                    delete props.others;
                    this.get_order().showScreen(true);
                } else {
                    name = "ProductScreen";
                    props = undefined;
                    this.get_order().showScreen(true);
                }
            };
            if (name === "ReceiptScreen") {
                this.get_order().showScreen(false, true);
            };
        };
        super.showScreen(name, props);
    },
});
