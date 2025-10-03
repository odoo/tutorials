import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    add_new_order() {
        const currentOrder = this.get_order();
        if (currentOrder?.state === "pay_later") {
            return currentOrder;
        }
        return super.add_new_order(...arguments);
    }
});
