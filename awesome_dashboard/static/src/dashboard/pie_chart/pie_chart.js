import { Component, useRef, onWillStart, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        data: Object
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        this.action = useService("action");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
    }
    
    renderChart() {
        this.chart?.destroy();
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data)
                }],
            },
            options: {
                onClick: (_, arr) => this.onChartClick(arr)
            }
        });
    }

    onChartClick(arr) {
        if (arr.length === 0) {
            return; // Graph currently reloading
        }
        const element = Object.values(this.props.data)[arr[0].index];
        if (!element || !element.action) {
            return; // No callback defined for this key
        }
        this.action.doAction(element.action);
    }
}
