import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    setup() {
        super.setup(...arguments);
    },

    set_employee(employee) {
        this.update({ service_employee_id: employee });
    },

    get_employee() {
        return this.service_employee_id;
    },

    getDisplayData() {
        const data = super.getDisplayData()
        return {
            ...data,
            employeeName: this.get_employee()?.name || ""
        }
    }
})
