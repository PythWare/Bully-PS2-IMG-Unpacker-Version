This unpacker script is for the IMG container files that the PS2 version of Bully uses. Credit goes to God(Christian) and myself for the coding. Bully's IMG container files contain the file data for files and the metadata for those files is within the DIR files. DIR files contain the file offset, file size, and filename for files within the IMG container files but to get the actual file offsets and file size you bit shift the file offset and file size to the left by 11. 

The formats for the IMG and DIR files:

DIR metadata file:

File offset within the IMG files 4 bytes(calculated by bit shifting the value to the left by 11)

File size 4 bytes (calculated by bit shifting the value to the left by 11)

Filename up to 24 bytes(some files have longer names but the max filename length goes to 24)

IMG container file:

File data equal to the bit shifted file size

I don't think Rockstar will mind since this is for the PS2 version especially since PC version mods exist.
