# Tmux tips

## ~/.tmux.conf

Create a `~/.tmux.conf` file with this content to make `tmux` apply these
settings as default:

```conf
set -g mouse on
set -g pane-border-status top
set -g pane-border-format "#{pane_index} #{pane_current_command}"
set -g mode-keys vi
```

Explain:

- Enable mouse support.
- Put a pane status on its top border.
- Set the format of a pane's status as its index followed by the active shell
command, for example `"1 htop"`.
- Set the key binding scheme in copy mode to `"vi"` style.

NOTE: `tmux` only read this file once while starting the `tmux` server (when the
first `tmux` session is being created). To make sure the settings in this file
are read and being applied correctly, terminate all running `tmux` sessions
before making change to this file.

## Working with panes

With the above settings set in `~/.tmux.conf`, and assuming `Ctrl+b` is the
`prefix` key stroke, here're some tips on working inside a `tmux` session:

### Move between panes

- Using arrow keys: press `Prefix` then an arrow key to move in that key direction.
- Using pane index: press `Prefix q`, `tmux` will briefly show all panes' IDs as
big colored number in each pane, then while the number are still being shown,
quickly press that number key. `tmux` will then move to the pane with that
number.

### Copy mode

In Copy mode, tmux stop updating its active pane to let user operate on the
existing buffer, like searching or select/copy text.

To activate Copy mode, press `Prefix [`.

Top stop Copy mode (while in that mode), press `Enter` or `q`.

### Select text with mouse

To select text, click and drag the left mouse over the desired text to highlight
it (should be in yellow background). Release the mouse when done, and that text
will be copied into `tmux`'s clipboard.

Some program doesn't support live text select by mouse. In that case, activate
copy mode before selecting text.

*NOTE: the copied text work within its `tmux` session only. It can't be pasted
into anywhere else, for example Windows' Notepad or not-a-tmux shell.*

### Select text with keyboard

First, activate copy mode. Then use arrow keys to move to the start of the
desired text, press `Space` to start selecting (a yellow highlight will be
shown), then move the cursor to expand the selection and finally press `Enter`
to copy the selected text into `tmux`'s clipboard and also deactivate the copy
mode.

`vi` key scheme can also be used, such as `h j k l w b` for movement.

*NOTE: the copied text work within its `tmux` session only. It can't be pasted
into anywhere else, for example Windows' Notepad or not-a-tmux shell.*

### Paste the copied text

To paste the copied text, press `Prefix ]`, and the text will be pasted into the
current cursor position.

### Searching

First, activate copy mode. Then press `/` to search downward from the beginning
of the current buffer, or `?` to search upward from the bottom up.

### Execute shell commands in an existing session

Use `tmux`'s `send-keys` command to send a serie of text into a running session
and ended by `Enter` string to execute. This is useful for running a program in
a `tmux` session, and then we can terminate that program without terminating
that session, like leaving the session for other tasks.

For example, the following command execute `htop -t -s PERCENT_CPU` in the
second pane of the first window of a running `tmux`'s session named `monitor`:

```sh
tmux send-keys -t monitor:0.1 "htop -t -s PERCENT_CPU" Enter
```
