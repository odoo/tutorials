import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { SelectSalespersonButton } from "../control_buttons/select_salesperson_button/select_salesperson_button";
import { patch } from "@web/core/utils/patch";


patch(ActionpadWidget,{
    components: {
        ...ActionpadWidget.components,
        SelectSalespersonButton,
    },
})
