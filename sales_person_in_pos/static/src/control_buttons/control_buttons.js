import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalesPersonButton } from "../select_sales_person_button/sales_person_button";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalesPersonButton,
    },
});

patch(ControlButtons.prototype, {
    get salesperson() {
        return this.pos.get_order().getSalesperson();
    },
});
