```
crackme1  ---> ./crackme1
```

```
crackme2  ---> strings crackme2 => super_secret_password 

==> ./crackme2 super_secret_password

=> flag{if_i_submit_this_flag_then_i_will_get_points}

OR,

$ ltrace ./crackme2 PASS

__libc_start_main(0x804849b, 2, 0xfff4a0a4, 0x80485c0 <unfinished ...>
strcmp("PASS", "super_secret_password")                  = -1
puts("Access denied."Access denied.
)                                   = 15
+++ exited (status 1) +++
```

```
crackme3 ---> strings crackme3 => got a string, with type base64 => then decoded it
```
```diff

crackme4:
---------

$ ltrace ./crackme4 PASS

__libc_start_main(0x400716, 2, 0x7fff7d015728, 0x400760 <unfinished ...>
strcmp("my_m0r3_secur3_pwd", "PASS")                     = 29
printf("password "%s" not OK\n", "PASS"password "PASS" not OK
)                 = 23
+++ exited (status 0) +++

OR,

gef➤  info functions 
All defined functions:

Non-debugging symbols:
0x00000000004004b0  _init
0x00000000004004e0  puts@plt
0x00000000004004f0  __stack_chk_fail@plt
0x0000000000400500  printf@plt
0x0000000000400510  __libc_start_main@plt
+0x0000000000400520  strcmp@plt
0x0000000000400530  __gmon_start__@plt
0x0000000000400540  _start
0x0000000000400570  deregister_tm_clones
0x00000000004005a0  register_tm_clones
0x00000000004005e0  __do_global_dtors_aux
0x0000000000400600  frame_dummy
0x000000000040062d  get_pwd
0x000000000040067a  compare_pwd
0x0000000000400716  main
0x0000000000400760  __libc_csu_init
0x00000000004007d0  __libc_csu_fini
0x00000000004007d4  _fini
gef➤  b *0x0000000000400520
Breakpoint 1 at 0x400520
gef➤  r VALUE
Starting program: /home/kali/Desktop/CTF/THM/TryHackMe/Reversing ELF/crackme4 VALUE
Breakpoint 1, 0x0000000000400520 in strcmp@plt ()


[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── register ────
+$rax   : 0x00007fffffffded0  →  "my_m0r3_secur3_pwd"
$rbx   : 0x0               
$rcx   : 0x11              
$rdx   : 0x00007fffffffe37f  →  0x4c4f430074736574 ("VALUE"?)
$rsp   : 0x00007fffffffdeb8  →  0x00000000004006da  →  <compare_pwd+96>  eax, eax
$rbp   : 0x00007fffffffdef0  →  0x00007fffffffdf10  →  0x0000000000400760  →  <__libc_csu_init+0> push r15
$rsi   : 0x00007fffffffe37f  →  0x4c4f430074736574 ("VALUE"?)
+$rdi   : 0x00007fffffffded0  →  "my_m0r3_secur3_pwd"
$rip   : 0x0000000000400520  →  <strcmp@plt+0> jmp QWORD PTR [rip+0x200b12]        # 0x601038 <strcmp@got.plt>
$r8    : 0x0               
$r9    : 0x00007ffff7fe21b0  →  <_dl_fini+0> push rbp
$r10   : 0xfffffffffffff289
$r11   : 0x00007ffff7e16c20  →  <__libc_start_main+0> push r15
$r12   : 0x0000000000400540  →  <_start+0> xor ebp, ebp
$r13   : 0x0               
$r14   : 0x0               
$r15   : 0x0               
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000 
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ───
0x00007fffffffdeb8│+0x0000: 0x00000000004006da  →  <compare_pwd+96> VALUE eax, eax        ← $rsp
0x00007fffffffdec0│+0x0008: 0x0000000000000000
0x00007fffffffdec8│+0x0010: 0x00007fffffffe37f  →  0x4c4f430074736574 ("VALUE"?)
+0x00007fffffffded0│+0x0018: "my_m0r3_secur3_pwd"         ← $rax, $rdi
0x00007fffffffded8│+0x0020: "secur3_pwd"
0x00007fffffffdee0│+0x0028: 0x0000000000006477 ("wd"?)
0x00007fffffffdee8│+0x0030: 0x93984369cced1a00
0x00007fffffffdef0│+0x0038: 0x00007fffffffdf10  →  0x0000000000400760  →  <__libc_csu_init+0> push r15   ← $rbp
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ───
     0x400510 <__libc_start_main@plt+0> jmp    QWORD PTR [rip+0x200b1a]        # 0x601030 <__libc_start_main@got.plt>
     0x400516 <__libc_start_main@plt+6> push   0x3
     0x40051b <__libc_start_main@plt+11> jmp    0x4004d0
 →   0x400520 <strcmp@plt+0>   jmp    QWORD PTR [rip+0x200b12]        # 0x601038 <strcmp@got.plt>
     0x400526 <strcmp@plt+6>   push   0x4
     0x40052b <strcmp@plt+11>  jmp    0x4004d0
     0x400530 <__gmon_start__@plt+0> jmp    QWORD PTR [rip+0x200b0a]        # 0x601040 <__gmon_start__@got.plt>
     0x400536 <__gmon_start__@plt+6> push   0x5
     0x40053b <__gmon_start__@plt+11> jmp    0x4004d0
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ───
[#0] Id 1, Name: "crackme4", stopped 0x400520 in strcmp@plt (), reason: BREAKPOINT
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ──
[#0] 0x400520 → strcmp@plt()
[#1] 0x4006da → compare_pwd()
[#2] 0x400759 → main()
───────────────────────────────
```
```
crackme5:
---------

Same as crackme4 but here, register and function name (strncmp) is different.

or, 

ltrace ./crackme5
__libc_start_main(0x400773, 1, 0x7fff3ba87b78, 0x4008d0 <unfinished ...>
puts("Enter your input:"Enter your input:
)                                = 18
__isoc99_scanf(0x400966, 0x7fff3ba87a30, 0, 0x7fb1fc2e3f33 ->[prompts for input] PASS
) = 1
strlen("PASS")                                           = 4
strlen("PASS")                                           = 4
strlen("PASS")                                           = 4
strlen("PASS")                                           = 4
strlen("PASS")                                           = 4
strncmp("PASS", "OfdlDSA|3tXb32~X3tX@sX`4tXtz", 28)      = 1
puts("Always dig deeper"Always dig deeper
)                                = 18
+++ exited (status 0) +++
```

```
crackme6:
---------

Have to Use Ghidra: 1st lets go to main (intusion: main function should be GOLD) 

=> We noticed the use of `compare_pwd` 

=> We headed to that program, noticed the use of another function `my_secure_test`

=> We then again went to my_secure_test file then "analised the if else portion to get the password"

==> 1337_pwd

```

```
crackme7
--------

Same as before but here:

In main function: => 

        if (local_14 == 0x7a69) {
          puts("Wow such h4x0r!");
          giveFlag();
          
 ===> hex(0x7a69) = 31337 ==> pass
 
 $ ./crackme7
 
 :
 :
 :
 
 [>] 31337
 
 ........
 flag{much_reversing_very_ida_wow}
 
 ```
 
 ```
 crackme8:
 --------
 
 same as before in ghidra, in main =>
 
     if (iVar2 == -0x35010ff3) {
      puts("Access granted.");
      giveFlag();
      uVar1 = 0;
      
 => hex(-0x35010ff3) ==> -889262067  
 
 => ./crackme8 -889262067
 
 Access granted.
flag{at_least_this_cafe_wont_leak_your_credit_card_numbers}

```