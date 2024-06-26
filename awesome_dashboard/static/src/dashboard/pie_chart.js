/** @odoo-module **/

import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        label: {type: String, optional: true},
        data: Object
    }

    setup() {
        this.pieChartRef = useRef("pie_chart_ref");

        onWillStart(() => 
            loadJS("/web/static/lib/Chart/Chart.js")
        );

        onMounted(() => {
            new Chart( this.pieChartRef.el, {
                    type: 'pie',
                    data: {
                        labels: Object.keys(this.props.data),
                        datasets: [{
                            label: this.props.label,
                            data: Object.values(this.props.data),
                        }]
                    },
                    options: {
                        maintainAspectRatio: false,
                    }
            });
        });
    }
}
