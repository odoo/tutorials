import { SalespersonList } from '@salesperson_in_pos/salesperson_list/salesperson_list';
import { ControlButtons } from '@point_of_sale/app/screens/product_screen/control_buttons/control_buttons';
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { patch } from '@web/core/utils/patch';
import { useState } from '@odoo/owl';

patch(ControlButtons.prototype, {
    setup(){
        super.setup();
        this.state = useState({
            salesperson_id: null,
        });
    },
    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            return;
        }

        const currentSalesperson = currentOrder.salesperson_id || null; 
        const payload = await makeAwaitable(this.dialog, SalespersonList, {
            salesperson: currentSalesperson,
            getPayload: (newSalesperson) => newSalesperson || null,
        });
        this.state.salesperson_id = payload || null;
        currentOrder.salesperson_id = payload || null;
        return currentOrder.salesperson_id;

    }
})
