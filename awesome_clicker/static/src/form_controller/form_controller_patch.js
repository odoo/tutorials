import { FormController } from "@web/views/form/form_controller";
import { useClicker } from "../clicker_hook";
import { patch } from "@web/core/utils/patch";

const FormControllerPatch = {
    setup() {
        super.setup(...arguments);
        const clicker = useClicker();
        if (Math.random() < 0.1) {
            clicker.giveReward();
        }
    },
};

patch(FormController.prototype, FormControllerPatch);
