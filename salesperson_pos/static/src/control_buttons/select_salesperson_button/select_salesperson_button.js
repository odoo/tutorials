import { Component, onWillStart, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SalespersonList } from "../../app/screen/SalespersonList/SalespersonList";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

export class SelectSalespersonButton extends Component {
    static template = "salesperson_pos.SelectSalespersonButton";

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.salesperson = useState({ type: Object, defaultValue: null });
    }

    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            console.warn("No active order found.");
            return;
        }
        const currentSalesperson = currentOrder.get_salesperson();
        const payload = await makeAwaitable(this.dialog, SalespersonList, {
            salesperson: currentSalesperson,
            getPayload: (newSalesperson) => {
                currentOrder.setSalesPerson(newSalesperson);
            },
        });

        if (payload) {
            if (payload.id === this.salesperson.id) {
                this.salesperson.id = null;
                this.salesperson.name = "Salesperson";
                currentOrder.setSalesPerson(null);
            } else {
                this.salesperson.id = payload.id;
                this.salesperson.name = payload.name;
                currentOrder.setSalesPerson(payload);
            }
        }
    }
}
