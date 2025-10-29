import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "../clicker_hook";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        if (Math.random() < 0.05) {
            const clicker = useClicker();
            clicker.getReward();
        }
    },
});
