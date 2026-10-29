import { loadJS } from "@web/core/assets"
import { onWillStart, signal, useEffect } from "@odoo/owl"

export function useChart(descFn) {
    const canvasRef = signal.ref();

    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

    useEffect(() => {
        const canvas = canvasRef();
        if (canvas) {
            const chart = new Chart(canvas, descFn());
            return () => chart.destroy();
        }
    });

    return canvasRef;
}