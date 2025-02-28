import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    initialize(attributes, options) {
        super.initialize(attributes, options);
        if (!this.salesperson_id) {
            const defaultSalesperson = this.pos.employees.find(
                (employee) => employee.user_id[0] === this.pos.user.id
            );
            if (defaultSalesperson) {
                this.set_salesperson(defaultSalesperson);
            }
        }
    },
    
    set_salesperson(salesperson) {
        this.update({ salesperson_id: salesperson });
        console.log("Salesperson set:", salesperson ? salesperson.name : "None");
    },

    get_salesperson() {
        const salesperson = this.salesperson_id;
        console.log("Getting salesperson:", salesperson ? salesperson.name : "None");
        return salesperson;
    },
});
