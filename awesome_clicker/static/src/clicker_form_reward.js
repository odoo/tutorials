import { patch } from "@web/core/utils/patch";
import { FormRenderer } from '@web/views/form/form_renderer';
import { rewards } from "./clicker_rewards"
import { chooseReward } from "./utils.js"
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(FormRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        if (Math.random() <= 0.01) {
            this.clicker = useState(useService("awesome_clicker_service"));
            var reward = chooseReward(rewards, this.clicker.level);
            if (reward) {
                this.notification = useService("notification");
                const notificationRemove = this.notification.add(
                    reward.description,
                    {
                        type: "success",
                        sticky: true,
                        title: "Lucky you!",
                        buttons: [
                            {
                                name: "Accept",
                                onClick: () => {
                                    reward.apply(this.clicker);
                                    notificationRemove();
                                },
                            }]
                    }
                );
            }
        }
    }
});
