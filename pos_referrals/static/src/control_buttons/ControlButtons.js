import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { ReferredBy } from "./ReferredBy";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        ReferredBy,
    },
});
patch(ControlButtons.prototype, {
    get referredByName() {
        const referredByPartner = this.partner?.referred_by;
        return referredByPartner ? referredByPartner.name : "No Referrer";
    },
    get company_name() {
        return this.pos.get_order()?.config_id.display_name;
    }
});
