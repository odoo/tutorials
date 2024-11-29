import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
// import { GraphRenderer } from "@web/views/graph/graph_renderer";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: {type: Object},
    }


    setup() {
        this.canvas = useRef('canvas')
        onWillStart(() => 
            loadJS("/web/static/lib/Chart/Chart.js")
        )
        onMounted(() =>
            this.renderChart()
        )
    }

    renderChart(){
        const ctx = this.canvas.el;
        this.chart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: Object.values(this.props.data),
                }],
                labels: Object.keys(this.props.data),
            }
        });
    }
}
