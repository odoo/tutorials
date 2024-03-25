/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(id) {
    const ref = useRef(id);
    onMounted(() => ref.el.focus());
}

export function filterInPlace(array, condition) {
    // See: https://stackoverflow.com/a/37319954
    let i = 0, j = 0;

    while (i < array.length) {
        const val = array[i];
        if (condition(val, i, array)) array[j++] = val;
        i++;
    }

    array.length = j;
    return array;
}
