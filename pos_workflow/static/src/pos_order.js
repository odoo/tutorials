import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    get finalized() {
        return !["draft", "pay_later"].includes(this.state);
    }
});
