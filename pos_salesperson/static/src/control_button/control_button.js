import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons"
import { SelectSalesPersonButton } from "@pos_salesperson/select_salesperson_button/select_salesperson_button";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalesPersonButton,
    },
});

patch(ControlButtons.prototype, {
    get salesperson() {
        return this.pos.get_order()?.getSalesperson();
    },
});
