# Bash tips

## Capture the output of commands with subshell into a variable
To capture the output of a command or chain of commands and put it into a variable, use:
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

## Suppress leading tabs in here document
See [this](https://tldp.org/LDP/abs/html/here-docs.html#LIMITSTRDASH).

Put a hyphen after the here document symbol `<<`, and Bash will ignore leading tabs (*but not spaces*). This helps make scripts more readable.
```sh
print_err() {
	cat <<-ENDOFERR
		This is a multiple lines error message.
		It was created by using here document in Bash.
	ENDOFERR
}
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
## Use nested `read`
In the following code, there are 2 `read`, the first one picks up lines from the output of `ls` command, and the second one read the user response for a confirmation.

By default, `read` command use standard input (stdin) file handle, so when the second `read` try to get user response from stdin, it will instead pick up data from the output of `ls` command, which was redirect to the stdin of the `while` loop for the fist `read` (see the last line). Because there're still data ready to be read from stdin, the second `read` will return immediately with `response` picked up from stdin (which should be the second line) instead of waiting for real user input.

To avoid this problem, since user input always goes through stdin, we need to redirect the output of the `ls` command to a different file handle, which in our example below is `3` (see the last line), and tell the first `read` to pick up lines from that file handle, hence the `-u 3` option. 

Note that there are always 2 builtin file handle, which is `1` for `stdin` and `2` for both `stdout` and `stderr`. So, the first custom file handle available is `3`.

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
exec 9>$lock
echo Acquiring lock...
flock 9
echo Lock acquired.
# Put current PID to lock file.
echo $$ 1>&200
# TODO: Put the critical code here.
echo Do something
echo End.
```
The following script try to acquire the mutex but doesn't wait:
```sh
#!/bin/bash
set -e
scriptname=$(basename $0)
lock="/tmp/${scriptname}"
exec 9>$lock
echo Acquiring lock...
flock -n 9 || (
	echo Could not acquire the lock. Another process must be running.
	# Terminate the script.
	exit 1
)
echo Lock acquired.
# Put current PID to lock file.
echo $$ 1>&200
# TODO: Put the critical code here.
echo Do something
echo End.
```