import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "../useClicker";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments)
        if (Math.random() < 0.6) {
            const clicker = useClicker();
            clicker.giveReward()
        }
    }
})