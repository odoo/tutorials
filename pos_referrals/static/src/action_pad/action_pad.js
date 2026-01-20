import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { ReferredBy } from "../control_buttons/ReferredBy";
import { patch } from "@web/core/utils/patch";


patch(ActionpadWidget,{
    components: {
        ...ActionpadWidget.components,
        ReferredBy,
    },
})
patch(ActionpadWidget.prototype, {
    get referredByName() {
        const referredByPartner = this.pos.get_order()?.get_partner()?.referred_by;
        return referredByPartner ? referredByPartner.name : "No Referrer";
    },
    get company_name() {
        return this.pos.get_order()?.config_id.display_name;
    }
});
