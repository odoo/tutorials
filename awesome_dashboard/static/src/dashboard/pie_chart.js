/** @odoo-module **/

import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { rpc, loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = ["s?", "m?", "l?", "xl?", "xxl?"]

    setup() {
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        let pieRef = useRef("pie-canvas")
        onMounted(() => {
            new Chart(pieRef.el, {
                "type": "pie",
                "data": {
                    "labels": ["S", "M", "L", "XL", "XXL"],
                    "datasets": [{
                        "data": [
                            this.props["s"],
                            this.props["m"],
                            this.props["l"],
                            this.props["xl"],
                            this.props["xxl"],
                        ],
                    }],
                },
            });
        });
    }
}

