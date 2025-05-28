import { patch } from '@web/core/utils/patch';
import { Order } from '@point_of_sale/app/store/models';

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.sales_agent_id = null;
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.sales_agent_id = this.get_sales_agent();
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.set_sales_agent(json.sales_agent_id);
    },

    set_sales_agent(agent_id) {
        this.sales_agent_id = agent_id;
        this.trigger('change');
    },

    get_sales_agent() {
        return this.sales_agent_id;
    },
});
