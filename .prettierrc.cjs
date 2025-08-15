/** @type {import('prettier').Config} */
const config = {
    plugins: [require.resolve("@prettier/plugin-xml")],
    bracketSpacing: false,
    bracketSameLine: true,
    singleAttributePerLine: false,
    printWidth: 120,
    proseWrap: "always",
    semi: true,
    trailingComma: "es5",
    xmlWhitespaceSensitivity: "strict",
    tabWidth: 4,
    xmlSelfClosingSpace: false,
};

module.exports = config;
