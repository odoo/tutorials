/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";

export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList";
    static props = {
        selectCustomer: {
            type: Function,
        },
    };

    setup() {
        this.orm = useService("orm");
        onWillStart(async () => {
            this.partners = await this.orm.searchRead("res.partner", [], ["display_name"]);
        })
    }
}
