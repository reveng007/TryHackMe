
# THM: Classic Passwd
 ---------------
 --------------  

### Task 1  Get the flag:

> I forgot my password, can you give me access to the program?":

#### :arrow_right: We used ltrace (a library caller) which only works for elf file extension

```diff

+ $~> file Challenge.Challenge

Challenge.Challenge: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b80ce38cb25d043128bc2c4e1e122c3d4fbba7f7, for GNU/Linux 3.2.0, not stripped

+ $~> strings Challenge.Challenge 

/lib64/ld-linux-x86-64.so.2
strcpy
exit
__isoc99_scanf
puts
printf
__cxa_finalize
strcmp
__libc_start_main
libc.so.6
GLIBC_2.7
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
Made by H
4non
https://H
github.cH
om/n0obiH
AGB6js5dH
9dkGf
[]A\A]A^A_
+Insert your username: 
Welcome
+Authentication Error
+THM{%d%d}
;*3$"
GCC: (Debian 10.2.0-16) 10.2.0
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
Challenge.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
strcpy@@GLIBC_2.2.5
puts@@GLIBC_2.2.5
vuln
_edata
printf@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
__data_start
strcmp@@GLIBC_2.2.5
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
__isoc99_scanf@@GLIBC_2.7
exit@@GLIBC_2.2.5
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment

+ $~> ltrace ./Challenge.Challenge

printf("Insert your username: ")                      = 22
__isoc99_scanf(0x559f577e201b, 0x7fff3167ef50, 0, 0Insert your username: anything_we_like
)  = 1
strcpy(0x7fff3167eec0, "anything_we_like")            = 0x7fff3167eec0
strcmp("anything_we_like", "AGB6js5d9dkG7")           = 32
puts("\nAuthentication Error"
Authentication Error
)                        = 22
exit(0 <no return ...>
+++ exited (status 0) +++

+ $~> echo AGB6js5d9dkG7

AGB6js5d9dkG7

+ $~> echo AGB6js5d9dkG7 | ./Challenge.Challenge

Insert your username: 
Welcome
THM{65235128496}

+ $~> echo THM{65235128496}

THM{65235128496}
```

### In Challenge file, THM was there but with no value it...
```
+ $~> strings Challenge.Challenge | grep THM

THM{%d%d}

```
 
