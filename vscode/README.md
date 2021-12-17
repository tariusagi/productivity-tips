# Visual Studio Code tips

## Shortcut keys

### General

- Open Command pallette: `Ctrl + Shift + P`
- Open folder: `Ctrl + K, Ctrl + O`
- Open recent: `Ctrl + R`

### Display

- Toggle fullscreen: `F11`
- Toggle zen mode: `Ctrl + K Z` (shows only the current editor in fullscreen).

### Editor

- Copy current line: `Ctrl + C` (without making a selection).
- Cut current line: `Ctrl + X` (without making a selection).
- Copy line up: `Shift + Alt + Up Arrow`
- Copy line down: `Shift + Alt + Down Arrow`
- Create new line below: `Ctrl + Enter`
- Create new line above: `Ctrl + Shift + Enter`
- Move a line up: `Alt + Up Arrow`
- Move a line down: `Alt + Down Arrow`

### Tabs

- Move to previous tab: `Ctrl + PgUp`
- Move to next tab: `Ctrl + PgDown`
- Select tab from list: `Ctrl + Tab`
- Close tab: `Ctrl + W`

### Panels

- Toggle Explorer: `Ctrl + B` or `Ctrl + 0`
- Open preview panel: `Ctrl + K, V`
- Open preview tab: `Ctrl + Shift + V`
- Toggle terminal: ``Ctrl + ` ``
- Move to Explorer: `Ctrl + 0`
- Move to Editor: `Ctrl + 1`
- Move to Preview: `Ctrl + 2`

## Essential settings

To open JSON settings, open the Command pallette with `Ctrl + Shift + P`, type
`open settings` and choose the action from the dropdown, as shown in the picture
below:

![picture 1](../images/493121d3925ff5133cab461d686fd81f8abbc5d70e30d8cc2047ce5e0ead511b.png)  

Set these settings using VS Code UI with `Ctrl + ,` or `settings.json`:

```json
	"editor.insertSpaces": false,
	"editor.tabSize": 2,
	"editor.rulers": [ 80	],
```

## Useful extensions

### [Todo Tree by Gruntfuggly](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)

MUST HAVE extension!

Add "NOTE" to the tree by adding it to `todo-tree.general.tags` list in VS
Code's `settings.json` like this:

```json
	"todo-tree.regex.regexCaseSensitive": false,
	"todo-tree.general.tags": [
		"BUG",
		"HACK",
		"FIXME",
		"TODO",
		"XXX",
		"NOTE",
		"UZI"
	],
```

This helps put all of my personal notes into the Todo tree so I can quickly jump
to review them.

### [markdownlint by David Anson](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)

Should include this `.markdownlint.json` to ignore code blocks while linting:

```json
{
	"MD010": {
		"code_blocks": false
	},
	"MD013": {
		"code_blocks": false
	}
}
```

Or put this section into VS Code's User or Workbench's `settings.json`:

```json
	"markdownlint.config": {
		"default": true,
		"MD010": {
			"code_blocks": false
		},
		"MD013": {
			"code_blocks": false
		}
	},
```

### [Markdown Image by Hancel.Lin](https://marketplace.visualstudio.com/items?itemName=hancel.markdown-image)

This is a amazing extension, which allows pasting image directly from clipboard,
and automatically create a `./images` directory at the same locatin as the
markdown file, then put the pasted image there in PNG format, with a name after
the picture's hash, such as
`fed088fc9006b5fc692d4403c4ef70c8f283aac4f6257a0407a7b0f46c01c237.png`

### [Highlight by Fabio Spampinato](https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-highlight)

This extension automatically highlight texts such as notes, todos, bugs...

### [Markdown Preview Enhanced by Yiyi Wang](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)

A MUST HAVE, amazing extension for Markdown documents. Right-click on the
preview to access more functionalities such as open in browser, export to PDF,
changing preview theme (especially GitHub themes)...
