import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "../clicker_hook/clicker_hook";

const patchFormController = {
    setup(){
        super.setup(...arguments)
        if(Math.random() < 0.1)
            {
                
                useClicker().giveReward();
            }
    }
}
patch(FormController.prototype, patchFormController);

