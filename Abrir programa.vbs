Set WshShell = CreateObject("WScript.Shell")

' Verificar se customtkinter está instalado
checkCommand = "python -c ""import customtkinter; print('ok')"" > nul 2>&1"
result = WshShell.Run("cmd /c " & checkCommand, 0, True)

' Se não tem, instalar silenciosamente
If result <> 0 Then
    WshShell.Run "cmd /c pip install customtkinter pillow > nul 2>&1", 0, True
End If

' Executar o programa principal
WshShell.Run "python gerenciador_senhas.py", 0