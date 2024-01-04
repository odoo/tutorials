/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(elementName) {
    const referenceElement = useRef(elementName);
    onMounted(() => {
        referenceElement.el.focus();
    });
}