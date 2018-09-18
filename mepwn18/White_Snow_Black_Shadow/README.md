Open file in hex-editor change ZIP signature to `\x50\x4b\x03\04` 
```
7z l -slt flag.zip 
zipdetails flag.zip 
zipinfo flag.zip 
zip -FF flag.zip --out fixed.zip 
7z -x flag.zip 
```

Now you'll get a PDF file, but corrupted and when you run PDF tools getting error but mutool can do the trick for you: 
`mutool extract message.pdf` 

by openning the out.pdf we see some text which says remove any other stuff from PDF, so basically if we remove all the stuff only thing remain is text:

pdf2text out.pdf

flag: `CTF{T3xt_Und3r_t3Xt!!!!}` 
