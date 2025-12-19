import { useRef, onMounted } from "@odoo/owl";


export function useAutoFocus(ref_name)
{
    const inputRef = useRef(ref_name);
        onMounted(() => {
            inputRef.el.focus();
        });
}