import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    set_salesperson(salesperson) {
        if (!salesperson) {
            return;
        }

        try {
            this.update({ salesperson_id: salesperson.id });
        } catch (err) {
            throw Error("Error updating salesperson_id:", err);
        }
    },
});
