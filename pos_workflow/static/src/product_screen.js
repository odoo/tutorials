import { _t } from "@web/core/l10n/translation";
import { onWillRender } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { ask } from "@point_of_sale/app/store/make_awaitable_dialog";

patch(ProductScreen.prototype, {
    async createOrderPosted() {
        if (
            !this.currentOrder.get_partner()
        ) {
            const confirmed = await ask(this.dialog, {
                title: _t("Please select the Customer"),
                body: _t(
                    "You need to select the customer before you can invoice or ship an order."
                ),
            });
            return false;
        }
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
