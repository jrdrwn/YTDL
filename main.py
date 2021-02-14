from os import system

from youtube_dl import YoutubeDL, utils


RMV = "\033[A\033[2K"


class MyLogger:
    def debug(self, msg):
        if "Merging" in msg:
            print("Sedang menggabungkan video dengan audio")
        if (
            "f249" in msg or "f250" in msg or "f251" in msg
        ) and "Destination" in msg:
            print("Sedang mendownload audio")
        elif ".f" in msg and not "Deleting" in msg:
            print("Sedang mendownload video")

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def download(url):
    f = get_format(url)
    a = list(map(lambda x: int(x.split()[0]), f.splitlines()[1:]))

    print(f)

    while True:
        format_id = int(input("\a\n[format_id] ~> "))
        print(f"{RMV}\r{RMV}", end="\r")
        if format_id in a:
            break
        print("Mohon masukkan format_id dengan benar")

    system("clear")

    opt = {
        "format": f"{format_id}+249/{format_id}+250/{format_id}+251",
        "progress_hooks": [progress_hooks],
        "logger": MyLogger(),
    }

    with YoutubeDL(opt) as ytdl:
        ytdl.download([url])


def sizeof_fmt(num, afs=0, suffix="B"):
    units = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]
    try:
        num += afs
        for unit in units:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, "Yi", suffix)
    except:
        return "NULL"


def get_format(url):
    with YoutubeDL({"quiet": True}) as ytdl:
        meta = ytdl.extract_info(url, download=False)["formats"]
        afs = meta[0]["filesize"]
        meta = sorted(meta, key=lambda x: int(x["format_id"]))
        meta = list(
            map(
                lambda x: [
                    x["format_id"],
                    x["format_note"],
                    sizeof_fmt(x["filesize"], afs=afs),
                ],
                filter(lambda x: "p" in x["format_note"], meta),
            )
        )
        header = ["format_id", "resolusi", "size"]
        return utils.render_table(header, meta)


def progress_hooks(x):
    if x["status"] == "downloading":
        print(f"[download] {x['_percent_str']} {x['_speed_str']}", end="\r")
    elif x["status"] == "finished":
        print("Proses download telah selesai")


def start():
    system("clear")
    # download(url=URL)
    while True:
        url = str(input("\a[url] ~> "))
        print(f"{RMV}\r{RMV}", end="\r")
        if url:
            download(url.strip())
            print("Selesai")
            break
        print("Mohon masukkan url youtube!")


start()
