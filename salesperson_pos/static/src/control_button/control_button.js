/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {ControlButtons} from "@point_of_sale/app/screens/product_session/control_buttons/control_buttons";
import { SalespersonButton } from "../salesperson/salesperson_button";

patch(ControlButtons, "pos_salesperson_patch", {
    components:{
        ...ControlButtons.components,
        SalespersonButton,
    }
})