import json
import argparse
from openai import OpenAI
import os
import sys
import platform

path = 'DeepSeek/History.json'


def is_idle():
    if 'idlelib' in sys.modules:
        return True
    return False


def system_check():
    system_type = platform.system()
    if system_type == "Windows":
        return True
    return False


def system_clear():
    if not is_idle():
        if system_check():
            os.system("cls")
        else:
            os.system("clear")


def check_path(p):
    if not os.path.exists(p):
        os.makedirs(p)


def check_key():
    cfg = get_path()
    if not os.path.exists(cfg):
        key_path = input("请输入您的密钥文件路径:\n\t")
        with open(key_path, 'r', encoding='utf-8') as f1:
            key = f1.read()
            with open(cfg, 'w', encoding='utf-8') as f:
                f.write(key)

        if is_idle():
            print(f"这里是您的API_KEY：\n\n\t{key}\n\n请自行核对是否正确\n" \
                  "\n如正确，则您可以在备份后删除原key文件\n" \
                  f"\n以保证密钥不被泄露\n\n\n{line}\n\n")
        else:
            print("color")
            print(f"这里是您的API_KEY：\n\n\t{key}\n\n\033[31m请自行核对是否正确\033[0m\n" \
                  "\n如\033[31m正确\033[0m，则您可以在备份后删除原key文件\n" \
                  f"\n以保证密钥不被泄露\n\n\n{line}\n\n")

    else:
        with open(cfg, 'r', encoding='utf-8') as f:
            return f.read()


def get_path():
    appdata_path = os.getenv('APPDATA')
    return os.path.join(appdata_path, 'stv_config')


def rm_key():
    if input("您是否确定要删除程序密钥配置？(y/n)\n\t").lower() == 'y':
        if input("请再三考量您的行为, 并且您是否有备份?(y/n)\n\t").lower() == 'y':
            print("已删除对应密钥文件配置\n")
            os.remove(get_path())
            return True
        else:
            pass
    else:
        print("为您的理智点赞.\n")
        print(line)
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description="启动对话并设置初始温度值。")
    parser.add_argument('-t', '--temperature',
                        type=float, default=1.3, help="设置初始温度值，范围从0到1.5，默认为1.3")
    return parser.parse_args()


def rename_history():
    history_path = 'DeepSeek/History.json'
    backup_dir = 'DeepSeek/'
    base_backup_name = 'history.bak'
    backup_extension = '.json'

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    if os.path.exists(history_path):
        backup_path = os.path.join(backup_dir, f'{base_backup_name}.json')

        count = 1
        while os.path.exists(backup_path):
            backup_path = os.path.join(backup_dir, f'{base_backup_name}{count}.json')
            count += 1

        os.rename(history_path, backup_path)
        print(f"已成功重命名为 {backup_path}\n")
    else:
        with open(history_path, 'w', encoding='utf-8') as f:
            f.close()
        print("文件不存在，已创建新的历史记录\n")


def load_conversation_history(a):
    if a == -1:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return start_new_conversation()
    else:
        temp_path = r'DeepSeek'
        name1 = 'History.bak.json'
        name2 = f'History.bak{a}.json'
        if a == 0:
            name = name1
        else:
            name = name2

        temp_path = os.path.join(temp_path, name)
        print(temp_path)
        try:
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = f.read()
                print("Successful 1")
                f.close()

            print("Successful 2")
            messages = json.loads(data)

            temp_path = os.path.join('History', name)
            print(temp_path)
            for message in messages:
                print(f"Role: {message['role']}, Content: {message['content']}\n\n")
                with open(temp_path, 'a', encoding='utf-8') as f:
                    a = str(message) + '\n\n'
                    f.write(a)
                    f.close()
        except Exception as e:
            print(f"发生错误：\n{e}\n\n")


def save_conversation_history(messages):
    with open(path, 'w') as f:
        json.dump(messages, f, indent=4, ensure_ascii=True)


def start_new_conversation():
    return [{"role": "system", "content": "You are a helpful assistant."}]


def update_conversation_history(user_input):
    conversation_history = load_conversation_history(-1)
    conversation_history.append({"role": "user", "content": user_input})
    return conversation_history


def clear_conversation_history():
    with open(path, 'w') as f:
        json.dump(start_new_conversation(), f)


def set_temperature(new_temperature):
    global temperature_value
    temperature_value = new_temperature
    print(f"温度值已设置为： {temperature_value}")


line = '======================================================='
log_line = '==================='


def show_help():
    print("\n")
    print(f"{line}\n")
    print("\t/h\t显示此工具菜单")
    print("\t/st v\t重新设置模型温度参数为v")
    print("\t/clear\t清除当前对话组(不保留当前轮次对话历史)")
    print("\t/bye\t退出应用")
    print("\t/re\t重命名当前对话组")
    print("\t/load\t阅读某一次的对话历史，并转存为对应的解码后文本")
    print("\t/rm\t删除您的API密钥配置文件")
    print(f"\n{line}", end='\n\n\n')


import time

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

check_path('History')
check_path('DeepSeek')
model_name = r'deepseek-coder'

try:
    system_clear()

    your_key = check_key()

    client = OpenAI(api_key=f"{your_key}", base_url="https://api.deepseek.com")
    # 这里的 api 接口只需要符合 OpenAI 规范，一般来说都能用

    path = 'DeepSeek/History.json'

    temperature_value = 1.3  # [0, 1.5]

    args = parse_arguments()

    temperature_value = args.temperature

    print(f"当前温度值为: {temperature_value}")
    print(f"当前模型为: {model_name}")
    print("您可以输入 /h 来获取基础工具菜单")
    print("请开始您愉快的对话吧.\n")

    if __name__ == '__main__':
        while True:

            user_input = input("\n请输入您的消息:\n\t")

            if user_input.lower() in ['/bye']:
                print("结束对话.")
                break

            if user_input.lower() == '/clear':
                print("记忆已清除\n")
                clear_conversation_history()
                del user_input
                continue

            if user_input.lower() == '/re':
                print("对话历史已备份\n")
                rename_history()
                del user_input
                continue

            if user_input.lower() == '/load':
                load_conversation_history(int(input("请输入对话历史序号:\n\t")))
                print("\n\n")
                del user_input
                continue

            if user_input.lower() == '/rm':
                print("\n如您继续, 则在本次对话结束后，\n" \
                      "您的API_KEY将无法使用，届时需要您重新配置\n请您谨慎操作\n")
                rm_key()
                print(line, end='\n\n')
                del user_input
                continue

            if user_input.lower() == '/h':
                show_help()
                del user_input
                continue

            if user_input.lower().startswith('/st'):
                try:
                    new_temp = float(user_input.split()[1])
                    if 0 <= new_temp <= 1.5:
                        set_temperature(new_temp)
                    else:
                        print("温度不合法.[0, 1.5]\n")
                except (IndexError, ValueError):
                    print("请输入正确的数值！\n")
                del user_input
                continue

            conversation_history = update_conversation_history(user_input)

            response = client.chat.completions.create(
                model=f"{model_name}",  # 目前深度求索给了两个稳定模型，一个是-chat,另一个是-coder
                messages=conversation_history,
                temperature=temperature_value,
                stream=False
            )

            assistant_reply = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": assistant_reply})

            print(f"\n助手:\n{assistant_reply}", end='\n\n')

            save_conversation_history(conversation_history)


except KeyboardInterrupt:

    log_content = f"{log_line}{current_time}{log_line}\n程序被用户中断\n\n\n"
    with open('ErrorLog.txt', 'a', encoding='utf-8') as log:
        log.write(log_content)


except Exception as e:

    print("出现异常问题，错误报告已保存到./ErrorLog.txt")
    log_content = f"{log_line}{current_time}{log_line}\n{e}\n\n\n"
    with open('ErrorLog.txt', 'a', encoding='utf-8') as log:
        log.write(f"{e}")
