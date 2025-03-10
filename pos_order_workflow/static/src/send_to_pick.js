import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
    },

    async sendToPick() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            this.notification.add(_t("No active order found!"), { type: "warning" });
            return;
        }
        if (!currentOrder?.select_shipping_date) {
            const today = new Date().toISOString().split("T")[0];
            currentOrder.select_shipping_date = today;
            this.notification.add(_t("Shipping date set to: ") + today, {
                type: "success",
            });
            await this.pos.syncAllOrders(currentOrder);
        } else {
            currentOrder.select_shipping_date = false;
        }
    },
});
