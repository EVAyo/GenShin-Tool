
import webbrowser
import getpass

log_path = f"C:\\Users\\{getpass.getuser()}\\AppData\\LocalLow\\miHoYo\\原神\\output_log.txt"

if __name__ == '__main__':
    with open(log_path, 'r', encoding='utf-8') as log:
        for line in log.readlines():
            if line.startswith('OnGetWebViewPageFinish') and -1 != line.find('gacha'):
                webbrowser.open(line[23:-1])
                exit(0)
    print('Not Found.')
