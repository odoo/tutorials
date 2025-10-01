import { onWillRender } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        onWillRender(() => {
            // If its a shared order it can be paid from another POS
            if ((!["draft", "pay_later"].includes(this.currentOrder?.state))) {
                this.pos.add_new_order();
            }
        });
    },
    async createOrderPosted() {
        this.currentOrder.state = "pay_later";
        this.pos.addPendingOrder([this.currentOrder.id]);
        let syncOrderResult;
        try {
            syncOrderResult = await this.pos.syncAllOrders({ throw: true });
        }
        catch (error){
            console.error("Sync failed", error);
        }
    }
});
