import { registry } from '@web/core/registry';
import { ClickerModel } from './clicker_model';

const clickerService = {
    dependencies: ['effect'],
    start(_, { effect }) {
        const clicker = new ClickerModel();
        for (const milestone of clicker.milestones) {
            clicker.bus.addEventListener(
                milestone.event,
                () => {
                    effect.add({
                        type: 'rainbow_man',
                        message: milestone.description,
                    });
                }
            );
        }
        return clicker;
    }
};

registry.category('services').add('awesome_clicker.clicker', clickerService);
