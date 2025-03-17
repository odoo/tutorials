import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";

patch(PosStore.prototype, {
    async SelectSalesperson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            console.warn("No active order found.");
            return;
        }

        const salesperson_list = this.pos.models['hr.employee'].map((person) => ({
            id: person.id,
            item: person,
            label: person.name,
            isSelected: currentOrder.getSalesperson()?.id === person.id || false
        }));

        const currentSalesperson = await makeAwaitable(this.pos.dialog, SelectionPopup, {
            title: "Select A SalesPerson",
            list: salesperson_list,
        });
        
        if (currentSalesperson) {
            const existing_salesperson = currentOrder.getSalesperson();
            if (!(existing_salesperson?.id === currentSalesperson?.id)) {
                currentOrder.setSalesperson(currentSalesperson);      
            } else {
                currentOrder.setSalesperson(false);
            }
        }
    },
});
