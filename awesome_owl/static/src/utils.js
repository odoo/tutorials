import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(nameOfElementRef) {
    const targetElementRef = useRef(nameOfElementRef);
    onMounted(() => {
        const htmlElement = targetElementRef.el;
        if (htmlElement) htmlElement.focus();
    });
}
