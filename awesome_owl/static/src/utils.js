import { useRef, onMounted } from "@odoo/owl"

export function useAutofocus(refName) {
    const myRef = useRef(refName);
    onMounted(() => {
        myRef.el.focus();
    });
}
