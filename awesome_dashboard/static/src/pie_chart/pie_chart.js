/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object,
        label: String,
    }

    setup(){
        this.graphRef = useRef("graph");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.create_chart();
        });
    }

    create_chart() {
        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);
        this.chart = new Chart(this.graphRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: values,
                    }
                ],
            },
        });
    }
}
