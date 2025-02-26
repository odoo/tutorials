import { FormController } from '@web/views/form/form_controller';
import { patch } from '@web/core/utils/patch';
import { useService } from '@web/core/utils/hooks';
import { useClicker } from './utils';
import { choose } from './utils';

const rewards = [
    {
        description: "Get 1 click bot",
        apply: clicker => clicker.clickBot.count++,
        maxLevel: 3
    },
    {
        description: "Get 10 click bots",
        apply: clicker => clicker.clickBot.count += 10,
        minLevel: 3,
        maxLevel: 4
    },
    {
        description: "Increase bot power!",
        apply: clicker => clicker.power.count++,
        minLevel: 3,
        maxLevel: 5
    }
];


function getReward(clicker) {
    return choose(rewards, reward => {
        return  (!reward.minLevel || reward.minLevel <= clicker.level) &&
                (!reward.maxLevel || reward.maxLevel >= clicker.level);
    });
}

patch(FormController.prototype, {
    setup() {
        super.setup();
        const rewardProbability = .9; // TODO: change to .01
        if (Math.random() > rewardProbability) {
            return;
        }
        const clicker = useClicker();
        const reward = getReward(clicker);
        if (!reward) {
            return;
        }
        const notifService = useService('notification');
        const action = useService('action');
        const close = notifService.add(`Congrats, you won a reward: "${reward.description}"`, {
            sticky: true,
            type: 'success',
            buttons: [{
                name: 'Collect',
                onClick: () => {
                    reward.apply(clicker);
                    action.doAction({
                        type: 'ir.actions.client',
                        tag: 'awesome_clicker.client_action',
                        target: 'new',
                        name: 'Clicker' 
                    });
                    close();
                },
                primary: false
            }]
        });
    }
});
