import { patch } from "@web/core/utils/patch"
import { FormController } from "@web/views/form/form_controller"
import { useClicker } from "../utility";
import { useService } from "@web/core/utils/hooks";

export const rewards = [
    {
        description: "Get 1 click bot",
        apply(clicker) {
            clicker.getClickBot(1);
        },
        minLevel: 1,
        maxLevel: 3,
    },
    {
        description: "Get 10 click bot",
        apply(clicker) {
            clicker.getClickBot(10);
        },
        minLevel: 3,
        maxLevel: 4,
    },
    {
        description: "Increase bot power!",
        apply(clicker) {
            clicker.getPower(1);
        },
        minLevel: 3,
    },
];

export function getRandomReward(clicker) {
    let choices = rewards.filter(r => (r.minLevel === undefined || r.minLevel <= clicker.level) 
        && (r.maxLevel === undefined || r.maxLevel >= clicker.level));

    if(choices.length == 0) return null;

    return choices[Math.floor(Math.random() * choices.length)]
}

const randomRewardChance = 1;

patch(FormController.prototype, {
    setup() {
        super.setup();

        if(Math.random() <= randomRewardChance) {
            let clicker = useClicker();
            let reward = getRandomReward(clicker);
            if(!reward) return;
            
            this.notification = useService("notification");
            const closeNotification = this.notification.add(`"${reward.description}"`, {
                title: "Congrats, you won a reward ",
                type: "success",
                sticky: true,
                buttons: [
                    {
                        name: "Collect",
                        onClick: () => {
                            closeNotification();
                            reward.apply(clicker);
                        }
                    },
                ],
            });
        }
    }
})
