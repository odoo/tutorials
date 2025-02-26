import { registry } from '@web/core/registry';
import { reactive } from '@odoo/owl';

export const clickerService = {
    start() {
        const state = reactive({ clicks: 1000 });
        return {
            state,
            increment(inc) {
                state.clicks += inc;
            },
        };
    }
};

registry.category('services').add('clicker', clickerService);
