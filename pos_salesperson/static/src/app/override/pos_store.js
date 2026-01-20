import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { SalesPersonList } from "../SalesPersonList/SalesPersonList";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

patch(PosStore.prototype, {
  async selectSalesperson() {
    const currentOrder = this.get_order();
    if (!currentOrder) {
      return false;
    }
    const currentSalesperson = currentOrder.get_salesperson();
    const payload = await makeAwaitable(this.dialog, SalesPersonList, {
      salesperson: currentSalesperson || null,
      getPayload: (newPartner) => currentOrder.set_salesperson(newPartner),
    });

    if (payload) {
      currentOrder.set_salesperson(payload);
    } else {
      currentOrder.set_salesperson(false);
    }

    return currentSalesperson;
  },
});
