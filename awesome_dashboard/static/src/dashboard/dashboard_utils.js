/** @odoo-module **/

import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export const buildDynamicComponentList = (values) => {
    const hiddenIds = JSON.parse(localStorage.getItem('items') ?? '[]')
    const result = values.map(({ key, value, view, name }) => {
        if (view === 'chart') {
            return {
                id: key,
                name: name,
                Component: PieChartCard,
                size: 3,
                props: {
                    title: name,
                    value
                },
                isHidden: hiddenIds.includes(key)
            }
        }
        return {
            id: key,
            name: name,
            Component: NumberCard,
            size: 3,
            props: {
                title: name,
                value
            },
            isHidden: hiddenIds.includes(key)
        }
    })
    return result;
}