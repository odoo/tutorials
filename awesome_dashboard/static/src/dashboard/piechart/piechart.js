/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets"; 

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object,
        label: String
    }

    setup() {
        this.canva = useRef("canva")
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => this.renderChart());
    }

    renderChart() {
        this.myPieChart = new Chart(this.canva.el, {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        label: this.props.label,
                        data: Object.values(this.props.data)
                    },
                ],
            },
        });
    }
}
