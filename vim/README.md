# Vim tips
## Paste mode
When pasting text into Vim, the auto and smart indenting function may mess up the text. To avoid this, enable paste mode before pasting and disable it afterward.

To enable paste mode, while in Vim, run this command: `:set paste`. Then toggle insert mode with `i` key, paste the text, then disable paste mode with `:set nopaste`.