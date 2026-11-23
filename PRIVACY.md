# Privacy

zw-wild collects no data and sends nothing anywhere.

- Its wild pages store one flag in the viewer's own browser (localStorage key `zw-wild-photosensitivity-ok`) to remember that the photosensitivity warning was accepted. Nothing else is stored, and the flag never leaves the browser.
- The diagram widget loads the open-source mermaid library from esm.sh, as the Claude app does.
- The plugin runs no code by itself. In the directory version Claude runs no code for it either: it builds wild files by copying the included Markdown blocks. The folder and uploaded versions carry a small Python tool that runs locally only when the user asks, through the normal permission prompts.

Questions: https://github.com/STREALOK/zw-wild/issues
