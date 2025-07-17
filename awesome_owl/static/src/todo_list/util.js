import { useEffect, useRef } from "@odoo/owl";

export function useAutofocus(ref) {
  useEffect(() => {
      if(ref.el){
        ref.el.focus();
      }
    },{ref});
  }
