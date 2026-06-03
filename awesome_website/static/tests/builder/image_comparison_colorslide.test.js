import { expect, manuallyDispatchProgrammaticEvent, test } from "@odoo/hoot";
import { defineWebsiteModels, setupWebsiteBuilderWithSnippet } from "@website/../tests/builder/website_helpers";
import { contains, defineStyle } from "@web/../tests/web_test_helpers";
import { animationFrame, queryOne } from "@odoo/hoot-dom";

defineWebsiteModels();

test("Change slider handle color using the custom builder option", async () => {
    defineStyle(`* { transition: none !important; }`);
    await setupWebsiteBuilderWithSnippet("s_image_comparison", { loadIframeBundles: true });

    await contains(":iframe .s_image_comparison").click();

    expect("[data-label='Pick Slider Color']").toHaveCount(1);

    await contains("[data-label='Pick Slider Color'] .o_we_color_preview").click();

    await contains(".o-hb-colorpicker-popover .custom-tab").click();
    await animationFrame();

    const hexInput = queryOne(".o-hb-colorpicker-popover input[data-color-method='hex']");
    expect(hexInput).toBeDisplayed();
    hexInput.value = "#ff0000";
    await manuallyDispatchProgrammaticEvent(hexInput, "input", { bubbles: true });
    await animationFrame();

    expect(":iframe .s_image_comparison .o_image_comparison_handle").toHaveStyle({
        "background-color": "rgb(255, 0, 0)",
    });
});
