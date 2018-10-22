# Questions

## What's `stdint.h`?

Library for Integer types like int_8 or uint_16.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Fixed range of numbers. "u" stands for unsigned and means no negative numbers.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE: 8 bit = 1 Byte, DWORD: 32 bit = 4 Byte, LONG: 32 bit = 4 Byte, WORD: 16 bit = 2 Byte

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

First 2 Bytes are "B" and "M" in ASCII.

## What's the difference between `bfSize` and `biSize`?

bfSize is the whole Image and biSize is the BITMAPINFOHEADER.

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB with the origin at the upper left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount specifies the bits per pixel.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If it can't find a file.

## Why is the third argument to `fread` always `1` in our code?

Specifies how many elements we want to read. We only want one.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

The padding would be 3, because 3 pixels * 3 bytes per pixel * 3 padding = 12, which is a multiple of 4.

## What does `fseek` do?

fseek () function moves file pointer position to given location.

## What is `SEEK_CUR`?

Current position of the file pointer.

## Whodunit?

It was Professor Plum with the candlestick in the library.
