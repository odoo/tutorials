import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(name) {
    const elementRef = useRef(name);

    onMounted(() => {
        elementRef.el.focus();
    });

}
