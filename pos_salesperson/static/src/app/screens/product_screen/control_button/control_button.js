import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { SalesPersonButton } from "./salesperson_button/salesperson_button"

patch(ControlButtons,{
    components: {
        ...ControlButtons.components,  
        SalesPersonButton,            
    },
})
