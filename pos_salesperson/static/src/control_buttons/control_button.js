import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalesPersonButton } from "../select_salesman_button/select_salesman_button";

patch(ControlButtons, {
    setup() {
        this._super();
    },
    components: {
        ...ControlButtons.components,
        SelectSalesPersonButton,
    }
});
