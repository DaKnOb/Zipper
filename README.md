# Zipper
A Gzip / Zip / ... Performance and Efficiency Measurement Tool

-----

Zipper will determine the optimal amount of layers a compression 
tool like `zip(1)` or `gzip(1)` must run for a specific file size 
containing specific data.

## What does that mean?

- Zipper can let you know what is the most storage efficient 
way for compressing 1 GB of /dev/zero data.
- Zipper can let you know what is the most time efficient way
for compressing 2 MB of /dev/urandom data.
- Zipper can run benchmarks and let you know the fastest
compression tool in your computer.
- Much more

## Usage

In the current version of Zipper, there is no Command Line Interface
Or Graphical User Interface for changing parameters. They are all
hardcoded inside the script. Open up `zipper.py` with your favorite
editor.

`StartGB` - The initial file size to check for

`EndGB` - The maximum file size to check for

`StartZIP` - The minimum amount of compression layers to apply

`EndZIP` - The maximum amount of compression layers to apply

`ZipWith` - The tool to use, preceded by `|` (`|zip`,`|gzip`,...)

`SourceFile` - The file from which Zipper will read data

`UnitSize` - The units in which `StartGB` and `EndGB` are measured

## What it does
Essentially Zipper generates a CSV with every file size from `StartGB` to `EndGB`
after applying from `StartZIP` to `EndZIP` layers of compression with `ZipWith` in
data retrieved from `SourceFile`.

## Output
The output of Zipper is `size.csv` and `time.csv`, each containing the
file size and the time it took to run respectively. During its operation,
Zipper will create a lot of `.gz` files. These are required for measuring
the file size. Usually they will be really small, but make sure you have enough
disk space for running Zipper.

## Measurements
In the `stats` folder you can find some results of Zipper running in an
Intel i7-4770k Debian Computer.

## Known bugs
The current version of Zipper works perfectly on Linux, but does not work on
Mac OSX. This is because the Mac OSX version of `head(1)` does not consider a 
valid argument the `-c 1K` to read 1 KByte and needs `-c 1024`. 

## Disclaimer
This is a rapid prototype created in a few minutes in Python. In no way is it
ready for production use and there's a lot of room for improvement. If you have 
some time beging resolving issues or if you don't, wait until I have some time
so I can resolve the issues.
