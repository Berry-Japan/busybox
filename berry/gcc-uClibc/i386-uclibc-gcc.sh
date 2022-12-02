#!/bin/sh

while (( $# > 0 ))
do
  case $1 in
    -lm)
      options=("${options[@]}" "/usr/lib/uClibc/libm.a")
      ;;
    *)
      options=("${options[@]}" "$1")
      ;;
  esac
  shift
done

gcc -m32 -nostdlib -Wl,--dynamic-linker, -Wl,-rpath-link,/usr/lib -L/usr/lib,/usr/lib/uClibc/ -nostdinc -isystem /usr/include/uClibc/ -iwithprefix include /usr/lib/uClibc/crti.o /usr/lib/uClibc/crt1.o "${options[@]}" -lgcc /usr/lib/uClibc/crtn.o /usr/lib/uClibc/libc.a
