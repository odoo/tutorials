/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "./clicker_hook";


const FormControllerPatch = {

    setup() {
        super.setup(...arguments);
        const clicker = useClicker();

        if (Math.random() * 100 < 1)
            clicker.getReward();
    }
}

patch(FormController.prototype, FormControllerPatch)
