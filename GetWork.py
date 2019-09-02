import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model import Work, Video
import requests
from contextlib import closing
import time


def video_download(download_url, nickname, aweme_id):
    # 视频下载
    isotimeformat = '%Y-%m-%d'
    day = time.strftime(isotimeformat, time.localtime(time.time()))
    doc = './抖音视频/{}/{}'.format(day, nickname)
    if not os.path.exists(doc):
        os.makedirs(doc)

    filename = './抖音视频/{}/{}/{}.mp4'.format(day, nickname, aweme_id)
    try:
        with closing(requests.get(download_url, stream=True)) as r:
            chunk_size = 1024
            content_size = int(r.headers['content-length'])
            with open(filename, "wb") as f:
                n = 1
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    n += 1
                print('下载视频: {}'.format(filename))

        if os.path.exists(filename):
            return filename
        else:
            return None

    except Exception as f:
        print(f)


def get_work():
    # 数据库位置
    engine = create_engine("mysql+pymysql://root:pythonman@127.0.0.1/TikTok?charset=utf8")

    # 创建会话
    session = sessionmaker(engine)
    mySession = session()
    results = mySession.query(Work).all()

    for result in results:
        status = result.status
        if status == 0:
            id = result.id
            url = result.url
            host = result.Host
            connection = result.Connection
            x_tt_trace_id = result.x_tt_trace_id
            Cookie = result.Cookie
            X_Khronos = result.X_Khronos
            X_Gorgon = result.X_Gorgon

            headers = {
                'Host':host,
                'Connection': connection,
                'sdk-version': '1',
                'User-Agent': 'Aweme 7.7.0 rv:77019 (iPhone; iOS 12.3.1; zh_CN) Cronet',
                'x-tt-trace-id':x_tt_trace_id,
                'Accept-Encoding': 'gzip, deflate',
                'Cookie': Cookie,
                'X-Khronos': X_Khronos,
                'X-Gorgon': X_Gorgon,
            }
            rsp = requests.get(url, headers=headers, verify=False, allow_redirects=False)
            if rsp.status_code == 200:
                nickname = ''
                data = json.loads(rsp.text)
                works = data['aweme_list']
                if works is None:
                    pass
                else:
                    for work in works:
                        aweme_id = work['aweme_id']
                        title = work['desc']
                        nickname = work['author']['nickname']
                        download_url = work['video']['play_addr']['url_list'][0]
                        result = mySession.query(Work).filter_by(id=aweme_id).first()
                        if result is None:
                            try:
                                result = mySession.query(Video).filter_by(aweme_id=aweme_id).first()
                                if result is None:
                                    video_download(download_url, nickname, aweme_id)
                                    video = Video(aweme_id=aweme_id, nickname=nickname, title=title)
                                    mySession.add(video)
                                    mySession.commit()

                            except Exception as f:
                                print(f)
                                pass
                        else:
                            print('视频已经存在')

                    mySession.query(Work).filter(Work.id == id).update({"status": "1", "user_name":nickname})
                    mySession.commit()


def run():
    get_work()


if __name__ == '__main__':
    run()