/** @odoo-module **/

import {onMounted, useRef} from "@odoo/owl"

export function useAutoFocus(inputRefName) {
    const inputRef = useRef(inputRefName);

    onMounted(() => {
        inputRef.el.focus();
    })
}
