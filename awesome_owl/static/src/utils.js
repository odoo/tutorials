/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl"

export const useAutofocus = (refName) => {
    const elementRef = useRef(refName)
    onMounted(() => {
        if(elementRef.el !== null) {
            elementRef.el.focus()
        }
    })

    return elementRef;
}