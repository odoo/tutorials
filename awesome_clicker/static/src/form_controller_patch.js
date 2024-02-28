/** @odoo-module */

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "./use_clicker";

const FormControllerPatch = {
    setup() {
        super.setup(...arguments);
        const clicker = useClicker();
        if (Math.random() < .01) {
            clicker.giveReward();
        }
    },
};

patch(FormController.prototype, FormControllerPatch);
