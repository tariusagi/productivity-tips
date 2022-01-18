# Bash tips

A great short reference to Bash can be found [here](https://www.computerhope.com/unix/ubash.htm).

The full document can be found [here](https://www.gnu.org/software/bash/manual/bash.html).

## Capture the output of commands with subshell into a variable

To capture the output of a command or chain of commands and put it into a
variable, use:

```sh
output=$([commands])
```

The `()` is called a *subshell*.

For example:

```sh
# Capture the list of files in current directory.
dir_list=$(ls -lh)
# Capture the list of TXT files.
txt_list=$(ls -lh|grep txt)
```

This syntax supports multiple lines:

```sh
txt_list=$(
  ls -lh |
  grep txt
)
```

## Group multiple commands

To run multiple commands without creating a subshell, use curly braces.
For example:

```sh
source /usr/local/lib/mylib.sh
test $? -eq 0 || { >&2 echo ERROR: library not found; exit 1; }
echo mylib.sh was loaded
```

Note that `{` and `}` are *keywords*, so they must be separated with the list of
commands by at least one space, and the last command must be follow by `;`
before the closing brace.

## Working with file descriptors and redirections

Should read [this](https://wiki.bash-hackers.org/howto/redirection_tutorial)
first.

Here're some common tips:

### Output to stderr

```sh
>&2 echo This is an error message
```

This command first duplicate `stderr` (file descriptor number `2`) into `stdout`
(file descriptor number `1`, which is default before the `>` operator, thus can
be omitted), which efficiently make anything go to `stdout` now go to whatever
`stderr` is pointing at, for the next command in effect. So after that, when
`echo` print something (default go to `stdout`), its output actually go to the
`stderr`.

### Discard stdout

```sh
command >/dev/null
```

The above line redirect `command`'s `stdout` (omitted since it is default) to
`/dev/null`, effectively discard all of its output.

### Discard stderr

```sh
command 2>/dev/null
```

The above line redirect `command`'s `stderr` to `/dev/null`, effectively discard
all of its output.

### Close file descriptor

Just make a duplicate of `-`. For example:

```sh
<&-  # Close stdin.
>&-  # Close stdout.
2>&- # Close sderr.
9>&- # Close file descriptor 9.
```

## Suppress leading tabs in here document

See [this](https://tldp.org/LDP/abs/html/here-docs.html#LIMITSTRDASH).

Put a hyphen after the here document symbol `<<`, and Bash will ignore leading
tabs (*but not spaces*). This helps make scripts more readable.

```sh
print_err() {
	cat <<-ENDOFERR
		This is a multiple lines error message.
		It was created by using here document in Bash.
	ENDOFERR
}
```

## Disable parameter substitution in here document

Quoting or escaping the "limit string" at the head of a here document disables parameter substitution within its body. It is useful to generate script or program source code. Example:

```sh
VERSION=1.0

cat <<"EOM"
This is a Bash script.
It's version is $VERSION
EOM
```

Will literally output:

```txt
This is a Bash script.
It's version is $VERSION
```

instead of:

```txt
This is a Bash script.
It's version is 1.0
```

The same result can be achieved with escaping the limit string. Example:

```sh
VERSION=1.0

cat <<\EOM
This is a Bash script.
It's version is $VERSION
EOM
```

But this is not readable as using quotes. So quoting is prefered.

The dash can also be used with quoting or escaping limit string to suppress leading tabs. Example:

```sh
print_usage() {
	cat <<-"ENDOFERR"
		Usage: program [options]
		If $OPTIONS was defined, its will replace the command line arguments.
	ENDOFERR
}
```

## Do a loop for a number of times

If times of looping is fixed, use:

```sh
for i in {1..100}; do
	# Do something.
done
```

If times is in variable, use `seq`:

```sh
count=100
for i in $(seq $count); do
	# Do something
done
```

## Get a script's absolute path, directory and base name

```sh
#!/bin/bash
SCRIPT_FULLPATH=$(readlink -f $0)
SCRIPT_DIR="$(dirname $SCRIPT_FULLPATH)"
SCRIPT_NAME=$(basename $SCRIPT_FULLPATH)
```

## Handle commandline argument with `getopts`

```sh
#!/bin/bash
while getopts "n:v" opt; do
  case ${opt} in
		n)
			echo Hello $OPTARG, how are you?
			;;
		v)
			echo "Version 1.0"
			;;
		\?)
			echo "Invalid option \"$OPTARG\""
			exit
			;;
		:) 
			echo "Option \"$OPTARG\" requires an argument."
			exit
			;;
	esac
done

# Remove processed arguments. Remaining arguments start from $1.
shift $((OPTIND-1))
if [[ $# -gt 0 ]]; then
	echo First remaining argument is $1
fi
```

## Read a text file line by line

```sh
#!/bin/bash
n=0
while IFS= read -r line; do
	# Handle line
	echo Line $n: $line
	let n+=1
done < somefile.txt
```

## Read the output of a command line by line

```sh
#!/bin/bash
n=0
while IFS= read -r line; do
	# Handle line
	echo Line $n: $line
	let n+=1
done < <(ls -lh)
```

## Handle user response

```sh
#!/bin/bash
read -r -p "What is your choice (y/n)? " response
case $response in
	[yY])
		echo You have selected Yes.
		exit 0
		;;
	[nN])
		echo You have selected No.
		exit 0
		;;
	*)
		echo Your response \"$response\" is not supported.
		exit 1
		;;
esac
```

## Read user input inside a read loop

In the following code, there are 2 `read`, the first one picks up lines from the
output of `ls` command, and the second one read the user response for a
confirmation.

By default, `read` command use standard input (stdin) file handle, so when the
second `read` try to get user response from stdin, it will instead pick up data
from the output of `ls` command, which was redirect to the stdin of the `while`
loop for the fist `read` (see the last line). Because there're still data ready
to be read from stdin, the second `read` will return immediately with `response`
picked up from stdin (which should be the second line) instead of waiting for
real user input.

To avoid this problem, since user input always goes through stdin, we need to
redirect the output of the `ls` command to a different file handle, which in our
example below is `3` (see the last line), and tell the first `read` to pick up
lines from that file handle, hence the `-u 3` option.

Note that there are always 2 builtin file handle, which is `1` for `stdin` and
`2` for both `stdout` and `stderr`. So, the first custom file handle available
is `3`.

```sh
#!/bin/bash
n=0
while IFS= read -r -u3 line; do
	# Handle line
	echo Line $n: $line
	let n+=1
	read -r -p "Do you want to continue? ([y]/n)" response
	case $response in
		[nN])
			exit
			;;
		*)
			;;
	esac
done 3< <(ls -lh)
```

## Create a mutex with flock

Base on this [article](https://linuxaria.com/howto/linux-shell-introduction-to-flock).

The following script wait on a mutex created by `flock`:

```sh
#!/bin/bash
set -e
scriptname=$(basename $0)
lock="/tmp/${scriptname}"
exec {fd}>>$lock
echo $$: Acquiring lock...
flock $fd
echo $$: Lock acquired.
# Put current PID to lock file.
echo $$ 1>&$fd
	# Put the critical code here.
echo $$: Do something
sleep 10
echo $$: End.
```

Explaination:

- `set -e`: tell Bash to exit immediately on any non-zero exit code from any
pipeline. See [The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).
- `exec {fd}>$lock`: try to open a file at the path in `$lock` and assign the
file descriptor to the variable `fd`. This file is open in appending mode,
because we will put the PID of the locking instance, and we don't want it to be
truncated each time another instance try to open it (`flock` does not protect
the file content, it just use that file as a mean to manage the mutex).
- `flock $fd`: try to acquire a lock which tie to the file descriptor in `$fd`
with `flock` command. In default mode, `flock` will wait until the lock can be
acquired. Other option, like return immediately if the lock is still locked, is
shown further down. See [flock manpage](https://man7.org/linux/man-pages/man1/flock.1.html).
- `echo $$ 1>&$fd`: write running instance's PID in the lock file.

The following script try to acquire the mutex but doesn't wait:

```sh
#!/bin/bash
set -e
scriptname=$(basename $0)
lock="/tmp/${scriptname}"
exec {fd}>$lock
echo Acquiring lock...
flock -n $fd || (
	echo Could not acquire the lock. Another process must be running.
	# Terminate the script.
	exit 1
)
echo Lock acquired.
# Put current PID to lock file.
echo $$ 1>&$fd
# Put the critical code here.
echo Do something
echo End.
```

## Use ANSI colors

My [ansilib.sh](https://github.com/tariusagi/shellutils/blob/main/lib/ansilib.sh)
has a collection of functions to easily output ANSI colored texts and
backgrounds. Check the its source for usage. Run `./skeleton.sh -c -h` or
`./skeleton.sh -c -n Peter` for demonstration.
