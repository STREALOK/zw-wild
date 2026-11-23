# Privacy

zw-wild collects no data and sends nothing anywhere.

- Its wild pages store one flag in the viewer's own browser (localStorage key `zw-wild-photosensitivity-ok`) to remember that the photosensitivity warning was accepted. Nothing else is stored, and the flag never leaves the browser.
- The diagram widget loads the open-source mermaid library from esm.sh, as the Claude app does.
- The plugin runs no code by itself. Its skill can ask Claude to write a small Python tool from the included Markdown and run it locally, through the user's normal permission prompts.

Questions: https://github.com/STREALOK/zw-wild/issues
