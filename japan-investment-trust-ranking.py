import bs4
import requests


URL = "https://itf.minkabu.jp/ranking/best_ranking"

LINE_NOTIFY_TOKEN = ""


def main():
    line_notify = LineNotify()
    ranking_html = requests.get(URL)
    soup = bs4.BeautifulSoup(ranking_html.text, "html.parser")
    fund_name_list = []
    price_list = []
    rimawari_list = []
    for i in range(10):
        data = soup.find_all("div", attrs={"class": "ranking_name"})[i].text
        fund_name_list.append(data.replace("\n", ""))
    for i in range(20):
        data = soup.find_all("td", attrs={"class": "tar wsnw"})[i].text
        if i % 2 == 0:
            price_list.append(data.replace("\n", ""))
        else :
            rimawari_list.append(data.replace("\n", ""))
    for i in range(10):
        send_data = (
            "\n" + str(i+1) + "位"
            "\n" + "ファンド名：" + fund_name_list[i] +
            "\n" + "基準価額　：" + price_list[i] + 
            "\n" + "利回り　　：" + rimawari_list[i]
        )
        line_notify.send(send_data)


class LineNotify:

    def __init__(self):
        self.line_notify_token = LINE_NOTIFY_TOKEN
        self.headers = {"Authorization": f"Bearer {self.line_notify_token}"}

    def send(self, data):
        data = {"message": f" {data}"}
        requests.post("https://notify-api.line.me/api/notify", data=data, headers=self.headers)


if __name__ == "__main__":
    main()