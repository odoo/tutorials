import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {

    set_salesperson(salesperson_id) {
        if (!salesperson_id) {
            return;
        }
        this.update({ salesperson_id: salesperson_id });
    },

    get_salesperson() {
        return this.salesperson_id
    }
});
