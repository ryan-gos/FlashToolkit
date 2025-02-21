import shutil
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
import os
import requests



### 刷入流程 必须带1.检查连接 2.前后提示 3.关闭子窗口(仅某些) 4.正确刷入


current_version = 'V0.1.0-Beta'


def CheckADBConnection():
    try:
        result = subprocess.run("adb devices", capture_output=True, text=True, check=True)
        output = result.stdout

        if 'List of devices attached' in output:
            lines = output.strip().split('\n')
            if len(lines) > 1:
                return True
            else:
                return False


        else:
            return False  # adb command failed

    except subprocess.CalledProcessError:
        print("执行ADB命令时出错")
        return False
    # finally:
    #     threading.Timer(1, CheckADBConnection).start()




#FASTBOOT连接检查

def CheckFASTBOOTConnection():
    try:
        if subprocess.run("fastboot devices", shell=True, check=True, capture_output=True, text=True).stdout:
            return True
        else:
            return False
    except Exception:
        pass
    # finally:
    #     threading.Timer(1, CheckFASTBOOTConnection).start()

# 显示免责声明
def show_disclaimer():
    disclaimer_text = """
        软件正处于测试阶段   !!!!请连接网络使用!!!!
       1.使用风险 本软件（FlashToolkit）提供的功能涉及对设备的底层操作，包括但不限于解锁 Bootloader、刷入固件、执行 ADB 和 FASTBOOT 命令等。这些操作可能会导致设备损坏、数据丢失、系统无法启动或其他不可预见的后果。用户需自行承担使用本软件的所有风险。
       2.责任限制 本软件的开发者（RyanGos）不对因使用本软件导致的任何直接或间接损失负责，包括但不限于设备损坏、数据丢失、业务中断或其他经济损失。用户在使用本软件前应充分了解相关操作的风险，并自行备份重要数据。
       3.适用性 本软件仅供技术爱好者学习和研究使用，不适用于商业用途。用户应确保其使用行为符合当地法律法规，并遵守设备制造商的相关规定。
       4.无担保 本软件按“原样”提供，不提供任何形式的明示或暗示的担保，包括但不限于对适用性、可靠性、安全性或准确性的担保。开发者不保证本软件能够满足用户的所有需求，也不保证其功能不会中断或没有错误。
       5.用户责任 用户在使用本软件前应确保已充分了解相关操作的风险，并具备必要的技术知识。开发者不对因用户误操作导致的任何后果负责。
       6.修改与终止 开发者保留随时修改或终止本软件的权利，且无需提前通知用户。
       """
    agree = messagebox.askyesno("免责声明", disclaimer_text)
    if not agree:
        root.destroy()  # 如果用户不同意，关闭软件

def get_version():
    try:
        response = requests.get("https://announcement.ryan-gos.us.kg/version.txt")
        version = response.text.strip()
    except Exception as e:
        messagebox.showerror("错误", f"无法获取版本{e}")
    else:
        if version == current_version:
            messagebox.showinfo("提示", "暂无更新可用")
        else:
            update = messagebox.askyesno("新版本现已可用!", f"当前版本为{current_version}，最新版本{version}可用")
            if update:
                subprocess.run("start https://download.ryan-gos.us.kg", shell=True)
            else:
                pass
# 公告

def show_announcement():
    try:
        url = "https://announcement.ryan-gos.us.kg/announcement.txt"
        response = requests.get(url)
        announcement = response.text
    except Exception as e:
        pass
    except requests.exceptions.RequestException:
        pass
    else:
        with open("announcement.txt", "w", encoding="utf-8") as file:
            file.write(announcement)
    finally:
        with open("announcement.txt", "r", encoding="utf-8") as file:
            announce = file.read()
        label13 = tk.Label(root, text=announce, font=("Microsoft Yahei UI Bold", 12), fg="#ffad00", bg="#252323", wraplength=320, justify="left")
        label13.place(relx="0", rely="0.043", anchor="nw")
        threading.Timer(30, show_announcement).start()





#功能
class Feature:
    #解锁BL
    def UnlockBL(self):
        if not CheckFASTBOOTConnection():
            messagebox.showerror("错误", "未连接FASTBOOT")
            blocking
        else:
            pass
        subprocess.run("fastboot oem unlock", shell=True)
        messagebox.showinfo("提示", "请使用音量键选择UNLOCK THE BOOTLOADER，按电源键确认")

    #刷入Zip包
    def FlashZip(self):
        if CheckFASTBOOTConnection():
            pass
        else:
            messagebox.showerror("错误", "未连接FASTBOOT")
            blocking
        file_path = filedialog.askopenfilename(title="选择刷入的Zip包", filetypes=[("", "*.zip")])
        if file_path == "":
            messagebox.showerror("错误", "未选择文件")
        else:
            ContinueFlash = messagebox.askyesno("提示", "是否继续刷入?")
            if ContinueFlash == True:
                try:
                    messagebox.showinfo("提示", "刷入成功将会提醒您,窗口未响应为正常现象,请勿关闭窗口")
                    subprocess.run(f"fastboot update {file_path}", shell=True)
                    messagebox.showinfo("提示", "刷入结束")
                except Exception as e:
                    messagebox.showerror("错误", f"刷入失败{e}")
            else:
                pass
            messagebox.showinfo("提示", "刷写结束")

    def shell(self):
        if CheckADBConnection():
            os.system('start powershell -Command "powershell ../powershell/shell.ps1"')
        else:
            messagebox.showerror("错误", "未连接ADB")
            blocking


    def sideload(self):
        if not CheckADBConnection():
            messagebox.showerror("错误", "未连接ADB")
            blocking
        else:
            pass
        zip_file = filedialog.askopenfilename(title="请选择zip文件", filetypes=[("", "*.zip")])
        if zip_file == "":
            messagebox.showerror("错误", "未选择文件")
            blocking
        else:
            messagebox.showinfo("提示", "按下确定开始刷入,完成会自动弹出提示,窗口未响应为正常现象,请勿关闭窗口,请注意手机画面变化")
            os.system(f'start powershell -Command "adb sideload {zip_file}"')

    def advanced_reboot(self):
        if not CheckADBConnection():
            messagebox.showerror("错误", "未连接ADB")
            blocking
        else:
            ask_reboot = tk.Toplevel(root)
            ask_reboot.geometry("500x500")
            ask_reboot.title("重启设备")
            ask_reboot.iconphoto(False, tk.PhotoImage(file="../Images/icon.png"))
            label12 = tk.Label(ask_reboot, text="重启设备到哪里?", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
            label12.pack(pady=20)
            reboot_to = None

            def reboot_fastboot():
                nonlocal reboot_to
                reboot_to = "fastboot"
                ask_reboot.destroy()

            def reboot_no():
                nonlocal reboot_to
                reboot_to = "9008"
                ask_reboot.destroy()

            def reboot_recovery():
                nonlocal reboot_to
                reboot_to = "recovery"
                ask_reboot.destroy()

            def reboot_bootloader():
                nonlocal reboot_to
                reboot_to = "bootloader"
                ask_reboot.destroy()

            def reboot_system():
                nonlocal reboot_to
                reboot_to = "system"
                ask_reboot.destroy()

            button8 = ttk.Button(ask_reboot, text="Fastboot", command=reboot_fastboot)
            button8.place(relx=0.3, rely=0.5, anchor="center")

            button9 = ttk.Button(ask_reboot, text="9008", command=reboot_no)
            button9.place(relx=0.7, rely=0.5, anchor="center")

            button10 = ttk.Button(ask_reboot, text="恢复模式", command=reboot_recovery)
            button10.place(relx=0.3, rely=0.6, anchor="center")

            button11 = ttk.Button(ask_reboot, text="Bootloader", command=reboot_bootloader)
            button11.place(relx=0.7, rely=0.6, anchor="center")

            button18 = ttk.Button(ask_reboot, text="系统", command=reboot_system)
            button18.place(relx=0.5, rely=0.7, anchor="center")

        # 等待用户选择重启方式
            root.wait_window(ask_reboot)

            if reboot_to == "fastboot":
                subprocess.run("adb reboot fastboot", shell=True)
            elif reboot_to == "recovery":
                subprocess.run("adb reboot recovery", shell=True)
            elif reboot_to == "bootloader":
                subprocess.run("adb reboot bootloader", shell=True)
            elif reboot_to == "system":
                subprocess.run("adb reboot", shell=True)
            else:
                subprocess.run("adb reboot edl", shell=True)

    def fastboot_advanced_reboot(self):
        if not CheckFASTBOOTConnection():
            messagebox.showerror("错误", "未连接FASTBOOT")
            blocking
        else:
            ask_advanced_reboot = tk.Toplevel(root)
            ask_advanced_reboot.geometry("500x500")
            ask_advanced_reboot.title("重启设备")
            ask_advanced_reboot.iconphoto(False, tk.PhotoImage(file="../Images/icon.png"))
            label12 = tk.Label(ask_advanced_reboot, text="重启设备到哪里?", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
            label12.pack(pady=20)
            reboot_to = None

            def reboot_fastboot():
                nonlocal reboot_to
                reboot_to = "fastboot"
                ask_advanced_reboot.destroy()

            def reboot_no():
                nonlocal reboot_to
                reboot_to = "9008"
                ask_advanced_reboot.destroy()

            def reboot_recovery():
                nonlocal reboot_to
                reboot_to = "recovery"
                ask_advanced_reboot.destroy()

            def reboot_bootloader():
                nonlocal reboot_to
                reboot_to = "fastbootd"
                ask_advanced_reboot.destroy()

            def reboot_system():
                nonlocal reboot_to
                reboot_to = "system"
                ask_advanced_reboot.destroy()

            button8 = ttk.Button(ask_advanced_reboot, text="Fastbootd", command=reboot_fastboot)
            button8.place(relx=0.3, rely=0.5, anchor="center")

            button12 = ttk.Button(ask_advanced_reboot, text="9008(不一定有效)", command=reboot_no)
            button12.place(relx=0.7, rely=0.5, anchor="center")

            button10 = ttk.Button(ask_advanced_reboot, text="恢复模式", command=reboot_recovery)
            button10.place(relx=0.3, rely=0.6, anchor="center")

            button11 = ttk.Button(ask_advanced_reboot, text="Bootloader", command=reboot_bootloader)
            button11.place(relx=0.7, rely=0.6, anchor="center")

            button17 = ttk.Button(ask_advanced_reboot, text="系统", command=reboot_system)
            button17.place(relx=0.5, rely=0.7, anchor="center")

            # 等待用户选择重启方式
            root.wait_window(ask_advanced_reboot)

            if reboot_to == "fastboot":
                subprocess.run("fastboot reboot fastboot", shell=True)
            elif reboot_to == "recovery":
                subprocess.run("fastboot reboot recovery", shell=True)
            elif reboot_to == "bootloader":
                subprocess.run("fastboot reboot bootloader", shell=True)
            elif reboot_to == "system":
                subprocess.run("fastboot reboot", shell=True)
            else:
                subprocess.run("fastboot oem edl")












class PayloadFlash:
    def __init__(self):
        self.shared_variable = None
    def init(self):
        directory = "../payload"
        delete_directory = messagebox.askyesno("删除", "是否要清空payload文件夹?")
        if not delete_directory:
            pass
        else:
            shutil.rmtree(directory)
            os.makedirs(directory)
        payload_file = filedialog.askopenfilename(title="选择payload.bin", filetypes=[("", "*.bin")])
        if not payload_file:
            messagebox.showerror("错误", "未选择文件")
        else:
            pass
        if not CheckFASTBOOTConnection():
            messagebox.showerror("错误", "未连接FASTBOOT")
            blocking
        else:
            pass
        messagebox.showinfo("提示", "按下确定以提取payload.bin,可在payload文件夹查看,完成会自动弹出提示,窗口未响应为正常现象,请勿关闭窗口")
        subprocess.run(f"payload-dumper-go.exe -o ../payload {payload_file}", shell=True)
        messagebox.showinfo("提示", "提取结束")


        self.items = self.get_file_list(directory)
        self.vars = []
        payloadwindow = tk.Toplevel(root)
        self.shared_variable = payloadwindow
        payloadwindow.title("提取的分区")
        for i, item in enumerate(self.items):
            var = tk.BooleanVar()
            display_item = item[:-4] if item.endswith('.img') else item
            chk = ttk.Checkbutton(payloadwindow, text=display_item, variable=var)
            chk.grid(row=i // 3, column=i % 3, sticky=tk.W)
            self.vars.append(var)

        btn = ttk.Button(payloadwindow, text="刷入选择的分区", command=self.get_selected_items_flash)
        btn.grid(row=(len(self.items) // 3) + 1, column=0, columnspan=3, pady=10)
        all = ttk.Button(payloadwindow, text="刷入所有提取的分区", command=self.get_all_items)
        all.grid(row=(len(self.items) // 3) + 2, column=0, columnspan=3, pady=10)
        payloadwindow.iconphoto(False, tk.PhotoImage(file="../Images/icon.png"))
        return self.shared_variable

    def get_file_list(self, directory):
        try:
            files = os.listdir(directory)
            files = [file for file in files if file != "autoflash.ps1"]
            return files
        except Exception as e:
            messagebox.showerror("错误", f"列出文件时出错: {e}")
            return []

    def get_all_items(self):
        folder_path = "../payload"
        filenames = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".img"):
                filenames.append(filename[:-4])  # 移除 .img 后缀
        flash_order = ['boot', 'dtbo', 'modem', 'reserve', 'recovery', 'vbmeta', 'vbmeta_system', 'abl', 'aop', 'bluetooth', 'cmnlib', 'cmnlib64', 'devcfg', 'dsp', 'hyp', 'imagefv', 'keymaster', 'LOGO', 'multioem', 'odm', 'oem_stanvbk', 'opproduct', 'qupfw', 'storsec', 'tz', 'uefisecapp', 'xbl', 'xbl_config', 'system', 'vendor', 'product']


        # 过滤出用户选择的分区并按照定义的顺序排序
        ordered_items = [item for item in flash_order if item in filenames]

        if not ordered_items:
            messagebox.showwarning("警告", "没有可刷入的分区")
            return
            # 如果需要包含其他类型的文件，可以取消以下注释并修改条件
            # else:
            #     filenames.append (filename)
        self.shared_variable.withdraw()
        if not CheckFASTBOOTConnection():
            messagebox.showerror("错误", "未连接FASTBOOT")
            blocking

        else:
            pass
        messagebox.showinfo("提示", "刷入完成将会提醒您,窗口未响应为正常现象,请勿关闭窗口")
        for i in ordered_items:
            if i == "vbmeta":
                subprocess.run("fastboot --disable-verity flash vbmeta ../payload/vbmeta.img", shell=True)
            elif i == "vbmeta_system":
                subprocess.run("fastboot --disable-verity flash vbmeta_system ../payload/vbmeta_system.img", shell=True)
                subprocess.run("fastboot reboot fastboot", shell=True)
            else:
                subprocess.run(f"fastboot flash {i} ../payload/{i}.img", shell=True)
        messagebox.showinfo("提示", "刷写结束")
        erase = messagebox.askyesno("格式化", "是否格式化设备?")
        if erase:
            subprocess.run("fastboot -w", shell=True)
        else:
            pass

        ask_reboot = tk.Toplevel(root)
        ask_reboot.geometry("500x500")
        ask_reboot.title("重启设备")
        ask_reboot.iconphoto(False, tk.PhotoImage(file="../Images/icon.png"))
        label12 = tk.Label(ask_reboot, text="重启设备到哪里?", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
        label12.pack(pady=20)
        reboot_to = None

        def reboot_system():
            nonlocal reboot_to
            reboot_to = "system"
            ask_reboot.destroy()

        def reboot_no():
            nonlocal reboot_to
            reboot_to = "none"
            ask_reboot.destroy()

        def reboot_recovery():
            nonlocal reboot_to
            reboot_to = "recovery"
            ask_reboot.destroy()

        def reboot_bootloader():
            nonlocal reboot_to
            reboot_to = "bootloader"
            ask_reboot.destroy()

        button8 = ttk.Button(ask_reboot, text="系统", command=reboot_system)
        button8.place(relx=0.3, rely=0.5, anchor="center")

        button9 = ttk.Button(ask_reboot, text="不重启", command=reboot_no)
        button9.place(relx=0.7, rely=0.5, anchor="center")

        button10 = ttk.Button(ask_reboot, text="恢复模式", command=reboot_recovery)
        button10.place(relx=0.3, rely=0.6, anchor="center")

        button11 = ttk.Button(ask_reboot, text="Bootloader", command=reboot_bootloader)
        button11.place(relx=0.7, rely=0.6, anchor="center")

        # 等待用户选择重启方式
        root.wait_window(ask_reboot)

        if reboot_to == "system":
            subprocess.run("fastboot reboot", shell=True)
        elif reboot_to == "recovery":
            subprocess.run("fastboot reboot recovery", shell=True)
        elif reboot_to == "bootloader":
            subprocess.run("fastboot reboot bootloader", shell=True)
        else:
            pass

        messagebox.showinfo("提示", "刷写结束")

    def get_selected_items_flash(self):
        selected_items = [item[:-4] if item.endswith('.img') else item for item, var in zip(self.items, self.vars) if var.get()]
        selected_tuple = tuple(selected_items)

        flash_order = ['boot', 'dtbo', 'modem', 'reserve', 'recovery', 'vbmeta', 'vbmeta_system', 'abl', 'aop', 'bluetooth', 'cmnlib', 'cmnlib64', 'devcfg', 'dsp', 'hyp', 'imagefv', 'keymaster', 'LOGO', 'multioem', 'odm', 'oem_stanvbk', 'opproduct', 'qupfw', 'storsec', 'tz', 'uefisecapp', 'xbl', 'xbl_config', 'system', 'vendor', 'product']


        # 过滤出用户选择的分区并按照定义的顺序排序
        ordered_items = [item for item in flash_order if item in selected_tuple]

        if not ordered_items:
            messagebox.showwarning("警告", "没有可刷入的分区")
            return


        messagebox.showinfo("已选择的分区:", "\n".join(selected_tuple))

        if not CheckFASTBOOTConnection():
            messagebox.showerror("错误", "未连接FASTBOOT")
            blocking
        else:
            pass
        selected_items_flashing = messagebox.askokcancel("继续", "是否继续刷入?")
        self.shared_variable.withdraw()
        if selected_items_flashing:
            messagebox.showinfo("提示", "刷入完成将会提醒您,窗口未响应为正常现象,请勿关闭窗口")
            for i in ordered_items:
                if i == "vbmeta":
                    subprocess.run("fastboot --disable-verity flash vbmeta ../payload/vbmeta.img", shell=True)
                elif i == "vbmeta_system":
                    subprocess.run("fastboot --disable-verity flash vbmeta_system ../payload/vbmeta_system.", shell=True)
                    subprocess.run("fastboot reboot fastboot", shell=True)
                else:
                    subprocess.run(f"fastboot flash {i} ../payload/{i}.img", shell=True)
            messagebox.showinfo("提示", "刷入完成")
            erase = messagebox.askyesno("格式化", "是否格式化设备?")
            if erase:
                subprocess.run("fastboot -w", shell=True)
            else:
                pass

            ask_reboot = tk.Toplevel(root)
            ask_reboot.geometry("500x500")
            ask_reboot.title("重启设备")
            ask_reboot.iconphoto(False, tk.PhotoImage(file="../Images/icon.png"))
            label12 = tk.Label(ask_reboot, text="重启设备到哪里?", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
            label12.pack(pady=20)
            reboot_to = None

            def reboot_system():
                nonlocal reboot_to
                reboot_to = "system"
                ask_reboot.destroy()

            def reboot_no():
                nonlocal reboot_to
                reboot_to = "none"
                ask_reboot.destroy()

            def reboot_recovery():
                nonlocal reboot_to
                reboot_to = "recovery"
                ask_reboot.destroy()

            def reboot_bootloader():
                nonlocal reboot_to
                reboot_to = "bootloader"
                ask_reboot.destroy()

            button8 = ttk.Button(ask_reboot, text="系统", command=reboot_system)
            button8.place(relx=0.3, rely=0.5, anchor="center")

            button9 = ttk.Button(ask_reboot, text="不重启", command=reboot_no)
            button9.place(relx=0.7, rely=0.5, anchor="center")

            button10 = ttk.Button(ask_reboot, text="恢复模式", command=reboot_recovery)
            button10.place(relx=0.3, rely=0.6, anchor="center")

            button11 = ttk.Button(ask_reboot, text="Bootloader", command=reboot_bootloader)
            button11.place(relx=0.7, rely=0.6, anchor="center")

            # 等待用户选择重启方式
            root.wait_window(ask_reboot)

            if reboot_to == "system":
                subprocess.run("fastboot reboot", shell=True)
            elif reboot_to == "recovery":
                subprocess.run("fastboot reboot recovery", shell=True)
            elif reboot_to == "bootloader":
                subprocess.run("fastboot reboot bootloader", shell=True)
            else:
                pass


            messagebox.showinfo("提示", "刷入完成")
        else:
            messagebox.showwarning("警告", "已取消刷入")



#创建窗口
feature = Feature()
show_disclaimer()
messagebox.showinfo("提示", "连接公告系统较慢,实在不行可以重启应用,按确定以继续")
get_version()
root = tk.Tk()
root.lift()
root.focus_force()
root.title("FlashToolkit")
root.geometry("1000x600")
root.configure(bg="#252323")
root.iconphoto(False, tk.PhotoImage(file='../Images/icon.png'))
show_announcement()


# Label
label1 = tk.Label(root, text="FASTBOOT专区", font=("Microsoft Yahei UI Bold", 20), bg="#252323", fg="grey")
label1.place(relx=0.83, rely=0.1, anchor="center")

label2 = tk.Label(root, text="ADB专区", font=("Microsoft Yahei UI Bold", 20), bg="#252323", fg="grey")
label2.place(relx=0.5, rely=0.1, anchor="center")

label3 = tk.Label(root, text="FASTBOOT连接状态:", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
label3.place(relx="0", rely="0.8", anchor="w")

label4 = tk.Label(root, text="ADB连接状态:", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
label4.place(relx="0", rely="0.85", anchor="w")

label6 = tk.Label(root, text="QQ群:364921039 网站:ryangos.us.kg", font=("Microsoft Yahei UI Bold", 11), bg="#252323", fg="#00ff17")
label6.place(relx="0.28", rely="1", anchor="se")

label8 = tk.Label(root, text="版本: V0.1.0-Beta公开测试", font=("Microsoft Yahei UI Bold", 11), bg="#252323", fg="grey")
label8.place(relx="0.8", rely="1", anchor="sw")

label9 = tk.Label(root, text="有bug请在QQ群反馈,或者有需要的改动可以提供建议", font=("Microsoft Yahei UI Bold", 9), bg="#252323", fg="grey")
label9.place(relx="0", rely="0", anchor="nw")

label10 = tk.Label(root, text="软件图标征求中,加群提交意见!!!", font=("Microsoft Yahei UI Bold", 11), bg="#252323", fg="grey")
label10.place(relx="0.887", rely="0.02", anchor="e")

label11 = tk.Label(root, text="服务器连接状态:", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="white")
label11.place(relx="0", rely="0.9", anchor="w")



if not CheckFASTBOOTConnection():
    label5 = tk.Label(root, text="未连接", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="#ff0000")
    label5.place(relx="0.16", rely="0.8", anchor="w")
else:
    label5 = tk.Label(root, text="已连接", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="#00ff17")
    label5.place(relx="0.16", rely="0.8", anchor="w")

if not CheckADBConnection():
    label7 = tk.Label(root, text="未连接", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="#ff0000")
    label7.place(relx="0.11", rely="0.85", anchor="w")
else:
    label7 = tk.Label(root, text="已连接", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="#00ff17")
    label7.place(relx="0.11", rely="0.85", anchor="w")




def change():
    try:
        url = "https://announcement.ryan-gos.us.kg/announcement.txt"
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            label15 = tk.Label(root, text="已连接", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="#00ff17")
            label15.place(relx="0.12", rely="0.9", anchor="w")
        else:
            pass
    except requests.exceptions.ConnectionError:
        label16 = tk.Label(root, text="未连接", font=("Microsoft Yahei UI Bold", 12), bg="#252323", fg="#ff0000")
        label16.place(relx="0.12", rely="0.9", anchor="w")
    threading.Timer(8, change).start()

threading.Thread(target=change, daemon=True).start()





#分割线
line = tk.Label(root, bg="grey")
line.place(relx=0.666, rely=0.5, anchor="center", width=1, height=1000)

line1 = tk.Label(root, bg="grey")
line1.place(relx=0.32, rely=0.5, anchor="center", width=1, height=1000)

line2 = tk.Label(root, bg="grey")
line2.place(relx=0, rely=0.04, anchor="nw", width=320, height=1)

line3 = tk.Label(root, bg="grey")
line3.place(relx=0, rely=0.77, anchor="sw", width=320, height=1)

line4 = tk.Label(root, bg="grey")
line4.place(relx=1.007, rely=0.04, anchor="e", width=340, height=1)



#按钮样式
style = ttk.Style()
style.configure("TButton", background="#252323", foreground="black", font=("Microsoft Yahei UI Bold", 15))

#按钮

newwindow = PayloadFlash()
## FASTBOOT专区
button1 = ttk.Button(root, text="一键解锁BL", command=feature.UnlockBL, padding=(50, 30))
button1.place(relx="0.83", rely="0.24", anchor="center")

button2 = ttk.Button(root, text="一键刷入Zip包", command=feature.FlashZip, padding=(50, 30))
button2.place(relx="0.83", rely="0.42", anchor="center")

button3 = ttk.Button(root, text="刷入payload.bin", command=newwindow.init, padding=(50, 30))
button3.place(relx="0.83", rely="0.6", anchor="center")

button7 = ttk.Button(root, text="高级重启", command=feature.fastboot_advanced_reboot, padding=(50, 30))
button7.place(relx="0.83", rely="0.78", anchor="center")
## ADB专区
button4 = ttk.Button(root, text="运行adb shell", command=feature.shell, padding=(50, 40))
button4.place(relx="0.5", rely="0.26", anchor="center")

button5 = ttk.Button(root, text="Sideload侧载", command=feature.sideload, padding=(50, 40))
button5.place(relx="0.5", rely="0.47", anchor="center")

button6 = tk.Button(root, text="检查更新", command=get_version, bg="#252323", fg="white", font=("Microsoft Yahei UI Bold", 8), relief="flat", padx=10, pady=10)
button6.place(relx="0.76", rely="0.98", anchor="center")

button9 = ttk.Button(root, text="高级重启", command=feature.advanced_reboot, padding=(50, 40))
button9.place(relx="0.5", rely="0.68", anchor="center")




def on_enter(event):
    widget = event.widget
    widget.config(text="恭喜你什么都没发现", fg="red")

def on_leave(event):
    widget = event.widget
    widget.config(text="RyanGos's FlashToolkit", fg="#0090ff")

label114514 = tk.Label(root, text="RyanGos's FlashToolkit", font=("Microsoft Yahei UI Bold", 15), bg="#252323", fg="#0090ff")
label114514.place(relx="0.5", rely="0.02", anchor="n")
label114514.bind("<Enter>", on_enter)
label114514.bind("<Leave>", on_leave)

def update_connection_status():
    # 检查 FASTBOOT 连接状态
    if CheckFASTBOOTConnection():
        label5.config(text="已连接", fg="#00ff17")

    else:
        label5.config(text="未连接", fg="#ff0000")

    # 检查 ADB 连接状态
    if CheckADBConnection():
        label7.config(text="已连接", fg="#00ff17")
    else:
        label7.config(text="未连接", fg="#ff0000")
    threading.Timer(1, update_connection_status).start()





threading.Thread(target=update_connection_status, daemon=True).start()

threading.Thread(target=show_announcement, daemon=True).start()

# threading.Thread(target=CheckADBConnection, daemon=True).start()
#
# threading.Thread(target=CheckFASTBOOTConnection, daemon=True).start()


root.resizable(False, False)
root.mainloop()