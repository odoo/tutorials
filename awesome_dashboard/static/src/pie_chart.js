import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";

import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";

    static props = {
        labels: {
            type: Array,
            element: {
                type: String
            }
        },
        data: {
            type: Array,
            element: {
                type: Number
            }
        },
        label: {
            type: String
        }
    }

    setup() {
        this.chart = useRef("pie_chart");

        onWillStart(async () => {
            await loadJS("https://cdn.jsdelivr.net/npm/chart.js");
        });

        onMounted(() => {
            new Chart(this.chart.el, {
                type: 'pie',
                data: {
                    labels: this.props.labels,
                    datasets: [{
                        label: this.props.label,
                        data: this.props.data,
                        borderWidth: 1
                    }]
                }
            });            
        });
    }
}
