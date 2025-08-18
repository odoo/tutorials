/** @odoo-module */

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";

export class settingDialog extends Component {
    static components = { Dialog };
    static template = "awesome_dashboard.settingDialog";

    setup() {
        this.cards_types = [
            {
                id: "average_quantity",
                description: "Average amount of t-shirt",
            },
            {
                id: "average_time",
                description: "Average time for an order to move state",
            },
            {
                id: "nb_new_orders",
                description: "Number of new orders",
            },
            {
                id: "nb_cancelled_orders",
                description: "Number of cancelled orders",
            },
            {
                id: "total_amount",
                description: "Total amount of new orders",
            },
            {
                id: "orders_by_size",
                description: "Total orders by size",
            }
        ];
        const initial_card_preference = JSON.parse(browser.localStorage.getItem("user_card_preference")) || [];
        this.selected_cards = useState(initial_card_preference);
    }

    static props = {
        close: Function,
        apply: { type: Function }
    };


    chooseCard(ev) {
        if (ev.target.checked) {
            this.selected_cards.push(ev.target.id)
        } else {
            if (this.selected_cards.indexOf(ev.target.id) !== -1) {
                const index = this.selected_cards.findIndex(card => card === ev.target.id);
                if (index >= 0) {
                    this.selected_cards.splice(index, 1);
                }
            }
        }
    }

    applyPreference() {
        this.props.apply(this.selected_cards, this.props.close)
    }

}
