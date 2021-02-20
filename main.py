import argparse

from youtube_dl import YoutubeDL, utils


class YoutubeDownloader:
    def __init__(self, url=None):
        self.url = url

    def download(self, url, type_url):
        if type_url == "video":
            f = self.get_format(url)
            a = list(map(lambda x: int(x.split()[0]), f.splitlines()[1:]))

            print(f)

            while True:
                format_id = int(input("\a\n[format_id] ~> "))
                if format_id in a:
                    break
                print("Mohon masukkan format_id dengan benar")

            opt = {
                "format": f"{format_id}+249/{format_id}+250/{format_id}+251",
                "progress_hooks": [self.progress_hooks],
                "logger": self,
            }
        elif type_url == "audio":
            opt = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "128",
                    }
                ],
            }

        with YoutubeDL(opt) as ytdl:
            ytdl.download([url])

    def get_format(self, url):
        with YoutubeDL({"quiet": True}) as ytdl:
            meta = ytdl.extract_info(url, download=False)["formats"]
            afs = meta[0]["filesize"]
            meta = sorted(meta, key=lambda x: int(x["format_id"]))
            meta = list(
                map(
                    lambda x: [
                        x["format_id"],
                        x["format_note"],
                        self.humanbytes(x["filesize"], afs=afs),
                    ],
                    filter(lambda x: "p" in x["format_note"], meta),
                )
            )
            header = ["format_id", "resolusi", "size"]
            return utils.render_table(header, meta)

    def humanbytes(self, num, afs=0, suffix="B"):
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

    def progress_hooks(self, x):
        if x["status"] == "downloading":
            print(
                f"[download] {x['_percent_str']} {x['_speed_str']}", end="\r"
            )
        elif x["status"] == "finished":
            print("Proses download telah selesai")

    def start(self):
        if self.url:
            self.download(self.url)
        else:
            while True:
                url = str(input("\a[url] ~> "))
                if url:
                    self.download(url.strip())
                    break
                print("Mohon masukkan url youtube!")
        print("Selesai")

    def debug(self, msg):
        if "Merging" in msg:
            print("Sedang menggabungkan video dengan audio")
        elif (
            "f249" in msg or "f250" in msg or "f251" in msg
        ) and "Destination" in msg:
            print("Sedang mendownload audio")
        elif ".f" in msg and not "Deleting" in msg:
            print("Sedang mendownload video")

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


yt = YoutubeDownloader()

parser = argparse.ArgumentParser(
    description="module untuk mendownload video/audio dari youtube.",
    usage="python3 main.py https://youtu.be/",
)
parser.add_argument(
    "url", type=str, help="url youtube yang ingin anda download"
)
parser.add_argument(
    "--type",
    "-t",
    type=str,
    help="hendak dijadikan apa url youtube-nya",
    choices=["video", "audio"],
    default="video",
)
args = parser.parse_args()

if args.url:
    yt.download(args.url, args.type)
else:
    yt.start()