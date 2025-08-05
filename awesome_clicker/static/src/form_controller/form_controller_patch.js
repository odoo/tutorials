import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useClicker } from "../clicker_hook";


const formControllerPatch = {
    setup(){
        super.setup(...arguments);
        if(Math.random() <= 0.01){
            const clicker = useClicker();
            clicker.getReward();
        }
    }
};

patch(FormController.prototype, formControllerPatch);
