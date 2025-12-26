import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useClicker } from "../utils";

const FormControllerPatch = {
    setup() {
        super.setup(...arguments);
        useClicker().giveRandomReward(0.01);
    },
};

patch(FormController.prototype, FormControllerPatch);
