import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { PartnerList } from "@point_of_sale/app/screens/partner_list/partner_list"
import { SalespersonList } from "./salesperson_list";
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/store/make_awaitable_dialog";

patch(PosStore.prototype, {
    async selectSalesPerson() {
        // FIXME, find order to refund when we are in the ticketscreen.
        const currentOrder = this.get_order();
        if (!currentOrder) {
            return false;
        }
        const currentPartner = currentOrder.get_salesperson();
        // if (currentPartner && currentOrder.getHasRefundLines()) {
        //     this.dialog.add(AlertDialog, {
        //         title: _t("Can't change customer"),
        //         body: _t(
        //             "This order already has refund lines for %s. We can't change the customer associated to it. Create a new order for the new customer.",
        //             currentPartner.name
        //         ),
        //     });
        //     return currentPartner;
        // }
        const payload = await makeAwaitable(this.dialog, SalespersonList, {
            partner: currentPartner,
            getPayload: (newPartner) => currentOrder.set_partner(newPartner),
        });

        if (payload) {
            currentOrder.set_partner(payload);
        } else {
            currentOrder.set_partner(false);
        }

        return currentPartner;
    },
});
console.log("POS Store Patched Loaded");
