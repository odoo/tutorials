import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { SelectSalesperson } from "./select_salesperson/select_salesperson";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalesperson,
    },
});