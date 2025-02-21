$root = Read-Host -Prompt "是否使用root身份运行shell?[y/n]"
switch ($root) {
    "y" { adb root }
    "n" { adb unroot }
}

$device = Read-Host -Prompt "是否指定设备?(一个设备时选n即可)[y/n]"
adb devices
switch ($device) {
    "y" { $serial = Read-Host -Prompt "请输入序列号"
adb -s $serial shell }
    "n" { adb shell }
}