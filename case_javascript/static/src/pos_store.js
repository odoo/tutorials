import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    getReceiptHeaderData(order) {
        return {
            ...super.getReceiptHeaderData(...arguments),
            congratulatory_text: this.config.congratulatory_text,
        }
    }
});