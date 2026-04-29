import { expect, test } from "@odoo/hoot";
import { contains } from "@web/../tests/web_test_helpers";
import {
    defineWebsiteModels,
    setupWebsiteBuilderWithSnippet,
} from "@website/../tests/builder/website_helpers";

defineWebsiteModels();

test("image comparison: set vertical slider", async () => {
    const { waitSidebarUpdated } = await setupWebsiteBuilderWithSnippet("s_image_comparison");
    await contains(":iframe .s_image_comparison").click();
    await waitSidebarUpdated();
    expect(".active[data-action-id='setCompareSliderDirection']")
        .toHaveAttribute("data-action-param", "horizontal");
    await contains(
        "[data-action-id='setCompareSliderDirection'][data-action-param='vertical']"
    ).click();
    expect(":iframe .s_image_comparison").toHaveClass("o_image_comparison_vertical");
});
