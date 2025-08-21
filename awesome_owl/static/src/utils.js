import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const myref = useRef(refName);
    onMounted(() => {
        myref.el.focus();
    });
}