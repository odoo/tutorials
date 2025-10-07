import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    set_salesperson(salesperson) {
        this.assert_editable();
        this.update({ salesperson_id: salesperson })
    },

    get_salesperson() {
        return this.salesperson_id;
    }
})
