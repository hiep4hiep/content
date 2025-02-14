# Change directory to the Traps installation folder
Set-Location "C:\Program Files\Palo Alto Networks\Traps"
 
# Disable Traps protection using cytool
Start-Process -FilePath "cytool.exe" -ArgumentList "protect disable" -Wait
 
# Enter the password when prompted
$securePassword = ConvertTo-SecureString "P@loalto5260" -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential -ArgumentList $securePassword
Start-Process -FilePath "cytool.exe" -ArgumentList "protect disable" -Credential $credential -Wait
 
# Uninstall Cortex XDR
Invoke-Expression "wmic product where `"`name like 'Cortex XDR%'`" call uninstall"