#!/bin/bash -e -E

: <<ENDOFCOPYRIGHT

================================================================================
 (C) Copyright 2013, Jaromir Sedlacek <jaromir.sedlacek@gmail.com>.

 All rights reserved.

 This is free software; you can redistribute it and/or modify it
 under the terms of the GNU Lesser General Public License (LGPL) as
 published by the Free Software Foundation; either version 3.0 of
 the License, or (at your option) any later version.

 This software is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU LGPL http://www.gnu.org/licenses/lgpl.html.
================================================================================

ENDOFCOPYRIGHT

# to have all functions in this library work correctly, you have to use "set -e -E" !!!

trap 'error "" ${LINENO}' ERR
trap 'cleanup "${clean[@]}"' EXIT

typeset prg=$(basename "$0")

function main() {
#
# main
#
	TMP=$(get_tmp)

	echo "pipestatus"
	false | :
	#pipestatus

	err 10 || error "Just error exit"

	echo "example function"
	init_d=
	etc=
	unset bin
	example
}

function example() {
#
# example function
#
	typeset fn="${FUNCNAME}"
	check_unset init_d etc bin

}

function check_unset() {
#
# check_unset [ <varname> [ <varname> ...]]
# returns 1 if any of variables <varname> are unset
#
	while [[ $# -gt 0 ]]; do
		if [[ "${!1+aAaAaAa}" != "aAaAaAa" ]]; then
			error "Variable $1 is not defined"
			return 1
		fi
		shift
	done
}

# to be able to remove all temp dirs, this array *MUST* be declared here
typeset clean=()

function toclean() {
#
# toclean [<dir> [<dir>] ...]
#	<dir>	directory to be automatically cleaned up on exit
#
	for dir in "$@"; do
		clean+="${dir}"
	done
}

function get_tmp() {
#
# get_tmp [<dir>]
#	
#	<dir>		prefix used for mkdir <dir>${RANDOM}
#
	typeset fn=${FUNCNAME}
	typeset tmp="$1"

	if [[ -z "${tmp}" ]]; then tmp="${TMP}"; fi
	if [[ -z "${tmp}" ]]; then tmp="${TEMP}"; fi
	if [[ -z "${tmp}" ]]; then
		if [[ -d "/tmp/" ]]; then
			tmp="/tmp/_"
		else 
			tmp=".tmp"
		fi
	fi
	# lets try 3 times, to get dir, to simple repeat statement
	tmp="${tmp}${RANDOM}"
	# create all parent directories
	typeset _tmp=$(dirname "${tmp}")
	mkdir -p "${_tmp}" || return 1
	mkdir "${tmp}" && { toclean "${tmp}"; echo "${tmp}"; return 0; }
	tmp="${tmp}${RANDOM}"
	mkdir "${tmp}" && { toclean "${tmp}"; echo "${tmp}"; return 0; }
	tmp="${tmp}${RANDOM}"
	mkdir "${tmp}" && { toclean "${tmp}"; echo "${tmp}"; return 0; }
	# we failed :(
	return 1
}

function pipestatus() {
#
# check all mebers of pipestatus and returns exit code of first failed
#
	for status in "${PIPESTATUS[@]}"; do
		if [[ $status -ge 0 ]]; then
			return $status
		fi
	done
	return 0
}

function cleanup() {
#
# cleanup [<dir> [<dir>] ...]
# removes all directorie and file in <dir>
#
	if [[ "${DEBUG}" != "keep" ]]; then
		for dir in "${@}"; do
			if [[ -n "${dir}" ]]; then
				rm -rf "${dir}"
			fi
		done
	fi
}

function err() {
#
# returns $1
#
	return $1
}

function error() {
#
#	$1		LINENO
#	$2		Error message
#	${prg}	Program name
#	${fn}	Function name
#
#	exist is [[ $? -gt 0 ]]
#
# 	err 10  || error "message" to display message and exit with exit code 10
#
	typeset err=${?}
	typeset ex
	typeset msg="${1:-Unhandled error}"
	typeset lineno="${2}"
	if [[ ${err:=0} -gt 0 ]]; then ex=$err; else unset ex; fi
	echo "ERROR:${prg:+ ${prg}:}${fn:+ ${fn}:} ${msg}${ex:+ (${ex})}${lineno:+ near line ${lineno}}." 1>&2
	if [[ ${err} -gt 0 ]]; then exit ${err}; fi
}

main "$@"
