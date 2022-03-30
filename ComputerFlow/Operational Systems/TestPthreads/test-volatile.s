	.file	"test-volatile.c"
	.text
	.p2align 4,,15
	.globl	fun
	.type	fun, @function
fun:
.LFB29:
	.cfi_startproc
	movl	sum(%rip), %eax
	addl	$10, %eax
	movl	%eax, sum(%rip)
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE29:
	.size	fun, .-fun
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"%d\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB30:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	subq	$80, %rsp
	.cfi_def_cfa_offset 96
	leaq	16(%rsp), %rbx
	movq	%fs:40, %rax
	movq	%rax, 72(%rsp)
	xorl	%eax, %eax
	movq	%rbx, %rdi
	call	pthread_attr_init@PLT
	leaq	fun(%rip), %rdx
	leaq	8(%rsp), %rdi
	xorl	%ecx, %ecx
	movq	%rbx, %rsi
	call	pthread_create@PLT
	movl	sum(%rip), %eax
	movq	8(%rsp), %rdi
	xorl	%esi, %esi
	addl	$5, %eax
	movl	%eax, sum(%rip)
	call	pthread_join@PLT
	movl	sum(%rip), %edx
	leaq	.LC0(%rip), %rsi
	xorl	%eax, %eax
	movl	$1, %edi
	call	__printf_chk@PLT
	movq	72(%rsp), %rcx
	xorq	%fs:40, %rcx
	jne	.L6
	addq	$80, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 16
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
.L6:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE30:
	.size	main, .-main
	.comm	sum,4,4
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
