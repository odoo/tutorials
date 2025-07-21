import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setSalesPerson(salesperson) {
        console.log("at pos order js level",salesperson);
        this.update({ salesperson_id: salesperson })
    },
    get_salesperson() {
        return this.salesperson_id;
    },
})
