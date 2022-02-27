##

from kokomi.miHoYo.HoYoLAB.dynamic import *

from 崩坏3壁纸 import *


def GetImages(post_id: int):
    data = GetPostFull(post_id)
    user = data["post"]["user"]

    # 子文件夹 uid+id
    subdir = to_ospath(user["uid"] + "_" + user["nickname"])
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    os.chdir(subdir)
    print(subdir)

    # 孙文件夹 id+标题
    subsubdir = to_ospath(str(post_id) + "_" + data["post"]["post"]["subject"])
    if not os.path.exists(subsubdir):
        os.mkdir(subsubdir)
    os.chdir(subsubdir)
    print(subsubdir)

    all_task = []
    with cf.ThreadPoolExecutor(max_workers=cpu_count()) as exec:
        # 遍历图片路径并下载
        imgs = data["post"]["image_list"]
        while len(imgs):
            url = str(imgs[0]["url"])
            all_task.append(
                exec.submit(download, url, url.split('/')[-1])
            )
            imgs.pop(0)
        cf.wait(all_task)

    # 保存响应体
    with open("image_list.json", "w", encoding='utf-8') as file:
        # file.write(data["post"]["image_list"])
        json.dump(data, fp=file, ensure_ascii=False, indent=4)

    print(f'all done。new {sum([task.result() for task in all_task])}。total {len(all_task)}')
    # 返回根路径
    os.chdir("../..")


if __name__ == "__main__":
    os.chdir('img')
    while True:
        post_id = int(str(input("post_id:")).split("/")[-1])
        GetImages(post_id)
