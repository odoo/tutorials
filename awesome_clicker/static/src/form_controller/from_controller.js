import { FormController } from '@web/views/form/form_controller';
import { patch } from "@web/core/utils/patch";

import { useClicker } from "../clicker_service";


patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        let clicker = useClicker();
        if (Math.random < 0.01) {
            clicker.getReward();
        }
    }
});
