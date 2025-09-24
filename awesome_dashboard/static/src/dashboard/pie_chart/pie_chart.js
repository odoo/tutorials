import { Component, onWillStart, useEffect, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        'data':{optional: false},
        'size': {type: Number, optional: true}
    }

    setup() {
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        this.ctx = useRef('pieChart')
        this.chart = null
        useEffect(() => {
            if(this.chart) {
                this.chart.destroy()
            }
            const dataset = {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data)
                }]
            }
            this.chart = new Chart(this.ctx.el, {type: 'pie', data: dataset})
        })
    }
}
