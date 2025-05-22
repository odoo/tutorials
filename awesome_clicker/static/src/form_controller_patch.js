import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";

import { useService } from "@web/core/utils/hooks";

import { useClicker } from "./clicker_service";
import { getReward } from "./click_reward";

patch(FormController.prototype, {
    setup() {
        if (Math.floor(Math.random()*2) == 1)
        {
            this.clicker = useClicker();
            const reward = getReward(this.clicker);
            if (reward) {
                this.notificationService = useService("notification");
                this.actionService = useService("action");
                this.notificationService.add(
                    "Congrats you won a reward: " + reward.description,
                    {
                        type: "success",
                        buttons: [
                            {
                                name: "Collect",
                                onClick: () => {
                                    reward.apply(this.clicker);
                                    this.actionService.doAction({
                                        type: 'ir.actions.client',
                                        name: 'Clicker',
                                        tag: 'awesome_clicker.client_action',
                                        target: 'new'
                                    });
                                }
                            }
                        ]
                    }
                );
            }
        }

        super.setup();
    },
});