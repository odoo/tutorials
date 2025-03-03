import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { SalespersonList } from "@pos_salesperson/salesperson_list";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

patch(PosStore.prototype, {
    async selectSalesPerson() {
        const currentOrder = this.get_order();
        if (!currentOrder) {
            return false;
        }
        const currentSalesperson = currentOrder.get_salesperson();
        const payload = await makeAwaitable(this.dialog, SalespersonList, {
            salesperson: currentSalesperson,
            getPayload: (newSalesperson) => currentOrder.set_salesperson(newSalesperson),
        });

        if (payload) {
            currentOrder.set_salesperson(payload);
        } else {
            currentOrder.set_salesperson(false);
        }
        return currentSalesperson;
    },
});
