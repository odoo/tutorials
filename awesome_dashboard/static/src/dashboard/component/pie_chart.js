import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.component.PieChart"
  static props = {
    title: String,
    data: Object,
  }

  setup() {
    this.chart = null;
    this.canvasRef = useRef("canvas");

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js")
    })

    useEffect(() => {
      this.renderChart()
      return () => {
        if (this.chart) this.chart.destroy()
      }
    })
  }

  renderChart() {
    const config = {
      type: "pie",
      data: this.props.data,
    }

    this.chart = new Chart(this.canvasRef.el, config)
  }
}
