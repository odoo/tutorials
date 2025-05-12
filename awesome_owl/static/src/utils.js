import { useRef, onMounted } from "@odoo/owl";


export function UseAutofocus(refString){
    const inputRef = useRef(refString);
    onMounted(() => {
        inputRef.el.focus();
    });
}
