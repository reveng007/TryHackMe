link: https://tryhackme.com/room/0x41haz

Other links: [SALE64 - Obfuscated shellcode and unique trick](https://pentester.blog/?p=247)

ELF Header: [Intro](https://will03.github.io/posts/ELF-Header-Introduction-PART-1/)


Write-up: https://muzec0318.github.io/posts/0x41haz.html

Used: 
> xxd -r => `-r` Converts hex dump into binary.

Used:
> rev => As the binary is LSB

```
$ echo "0x6667243532404032" | xxd -r | rev
2@@25$gf⏎                                                                                    

$ echo "0x40265473" | xxd -r | rev
sT&@⏎                                                                                        

$ echo "0x4c" | xxd -r | rev
L⏎ 
```


