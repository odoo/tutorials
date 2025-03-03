import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalesPersonButton } from "@pos_salesperson/salesperson_button";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    get salesperson() {
        return this.pos.get_order()?.get_salesperson();
    },
});
patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalesPersonButton,
    },
})
