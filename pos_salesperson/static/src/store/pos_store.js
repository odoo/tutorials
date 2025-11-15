import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

import { SalespersonList } from "@pos_salesperson/components/salesperson_list/salesperson_list";

patch(PosStore.prototype, {
    async setup(...args) {
        await super.setup(...args);
    },

    async selectSalesperson() {
        const currentOrder = this.get_order();
        if (!currentOrder) {
            return false;
        }

        const currentSalesperson = currentOrder.get_salesperson();

        const payload = await makeAwaitable(this.dialog, SalespersonList, {
            salesperson: currentSalesperson,
        });

        if (payload) {
            currentOrder.set_salesperson(payload);
        }else{
            currentOrder.set_salesperson(false);
        }

        return currentSalesperson;
    }
});
