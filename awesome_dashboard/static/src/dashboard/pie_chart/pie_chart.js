/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: Array,
        data: Array,
    };

    setup() {
        this.canvas = useRef('pie-canvas');
        onWillStart(async () => {
            await loadJS('/web/static/lib/Chart/Chart.js');
        });

        onMounted(() => {
            this.chart = new Chart(this.canvas.el, {
                type: 'pie',
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [
                        {
                            label: this.props.label,
                            data: Object.values(this.props.data),
                        },
                    ],
                },
            });
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });
    }
}