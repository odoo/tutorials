/** @odoo-module **/

import { Component, useRef, useEffect, onWillStart} from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class Piechart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        data: Array,
        labels: Array,
        slots: {type: Object, optional: true},
        size: Number,
    };

    /**
     * Instantiates a Chart (Chart.js lib) to render the graph according to
     * the current config.
     */
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie', 
            data: {
                labels: this.props.labels,
                datasets: [{
                    data: this.props.data,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
            }
        });
    }
    
    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        
        useEffect(() => this.renderChart());
    }
}