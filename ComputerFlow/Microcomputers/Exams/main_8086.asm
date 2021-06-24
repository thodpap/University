; Caclulcate factorial (n) 
read:
    in CX, [0500] ; Cx = input
    mov AX, 0001   ; Accumulator = 1
    mov DX, 0000   ; DX = 0
factorial:    
    mul CX  ; DX:AX = AX * CX
    sub CX, 0001 ; Cx -= 1
    loop factorial ; loop until Cx = 0

mov [0600], AX
mov [0601], DX
hlt ; stop execution