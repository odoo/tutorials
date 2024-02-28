/** @odoo-module */

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "./use_clicker";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        if (true){
            useClicker().getReward();
        }
    },
});