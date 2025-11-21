import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { AddQuantityButton } from "../add_quantity_button/add_quantity_button";

patch(ControlButtons, {
    setup() {
        super.setup();
    },
    components: {
        ...ControlButtons.components,
        AddQuantityButton,
    },
});
