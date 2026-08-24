from zlapi import ZaloAPI
from zlapi.models import *
import time
from concurrent.futures import ThreadPoolExecutor
import threading
import os
import sys

# Replace with your imei and cookies
imei = "cdacc641-6257-418c-9ee1-10961ff411a2-3d96f8e03a42123e5523adf5c57607ad"
cookies = {"zputm_source":"","zputm_medium":"","zputm_campaign":"","zpsrc":"","ZConsent":"timestamp=1787569981557&location=https://zalo.me/ott/","_gid":"GA1.2.1507840943.1787569982","__zi":"3000.SSZzejyD0jydXQckra00a3BBfxQL71AQV8UZjj1O4vvsZQ7-qrqSrNADgVdNNn_MCm.1","__zi-legacy":"3000.SSZzejyD0jydXQckra00a3BBfxQL71AQV8UZjj1O4vvsZQ7-qrqSrNADgVdNNn_MCm.1","_zlang":"vn","app.event.zalo.me":"8028641932241512930","_ga_YT9TMXZYV9":"GS2.1.s1787569934$o1$g1$t1787570918$j60$l0$h0","_ga_YS1V643LGV":"GS2.1.s1787570957$o1$g0$t1787570958$j59$l0$h0","_ga":"GA1.2.500963278.1787569934","_ga_3EM8ZPYYN3":"GS2.2.s1787569982$o1$g1$t1787570962$j60$l0$h0","zpsid":"Hcih.408854227.3._DkiUML2E0Yst6OGQK8u210nIZnLUW0zKN0AFywrQAv1wIRwP5yJX0z2E0W","zpw_sek":"CB0c.408854227.a0.AE902IXW_gYh5Nl5MOibtGEfGBPQiGUJ5iPtd2ZZG9Gy_N-q8CqEiZFPJOqvjXZ_1I3IZTwlZiEAYZZszE4btG"}


thread = ThreadPoolExecutor(max_workers=10000)


class WxBotWar(ZaloAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "-" # prefix bot có thể để trống
        self.idadmin = ["363636"] #adm id
        self.auto_chatting = False
        self.start_time = time.time()
        self.copy_mode = False
        self.copy_target = set()

    def sendTxt(self, filename, thread_id, thread_type):
        def auto_send():
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                if not lines:
                    self.sendMessage(Message(text="File khong co gi"), thread_id, thread_type)
                    self.auto_chatting = False
                    return

                index = 0
                while self.auto_chatting:
                    self.sendMessage(Message(text=lines[index]), thread_id, thread_type)
                    index = (index + 1) % len(lines) 
                    time.sleep(1) # Thời gian gửi tin nhắn
            except FileNotFoundError:
                self.sendMessage(Message(text=f"Not {filename}"), thread_id, thread_type)
                self.auto_chatting = False
            except Exception as e:
                self.sendMessage(Message(text=f"{str(e)}"), thread_id, thread_type)
                self.auto_chatting = False

        threading.Thread(target=auto_send).start()


    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        thread.submit(self.onHandle, mid, author_id, message, message_object, thread_id, thread_type)
        print(f"Tin nhan: {author_id}: {message}")
        # Copy mode:
        if self.copy_mode and author_id in self.copy_target:
            self.replyMessage(
                Message(text=message),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
    def onHandle(self, mid, author_id, message, message_object, thread_id, thread_type):
        # self.markAsDelivered(mid, message_object.cliMsgId, author_id, thread_id, thread_type, message_object.msgType)

        # Lệnh chức năng
        if message == f"{self.prefix}help":
            mention = Mention(author_id, length=7, offset=0)
            color = MessageStyle(style="color", color="cdd6f4", offset=0, length=3000, auto_format=False)
            smallfont = MessageStyle(style="font", size="13", offset=0, length=3000, auto_format=False)
            style = MultiMsgStyle([color, smallfont])
            ds_menu = """
            Danh sách lệnh:
            - {self.prefix}help: Hiển thị danh sách lệnh
            - {self.prefix}uid: Lấy UID của người dùng
            - {self.prefix}uptime: Xem thời gian hoạt động của bot
            - {self.prefix}reset: Khởi động lại bot
            - {self.prefix}1c: Chế độ 1c
            - {self.prefix}war: Chế độ war
            - {self.prefix}chui: Chế độ chửi
            - {self.prefix}so: Chế độ sớ
            - {self.prefix}nhay: Chế độ nhây
            - {self.prefix}copy: copy tin nhắn
            - {self.prefix}treo: Chế độ treo
            - {self.prefix}tagall: Tag tất cả thành viên trong nhóm

            """
            traloi = "@member "
            self.replyMessage(
                Message(text=traloi, style=style, mention=mention),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
        



        elif message.startswith(f"{self.prefix}uid"):
            if message_object.mentions:
                tagged_users = message_object.mentions[0]['uid']
            else:
                tagged_users = author_id
            response_message = f"{tagged_users}"
            message_to_send = Message(text=response_message)
            self.replyMessage(message_to_send, message_object, thread_id, thread_type)

        elif message.startswith(f"{self.prefix}uptime"):
            uptime = time.time() - self.start_time
            days, remainder = divmod(uptime, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
            self.sendMessage(Message(text=f"Uptime: {uptime_str}"), thread_id, thread_type)
        
        elif message.startswith(f"{self.prefix}reset"):
            self.sendMessage(Message(text="Đang khởi động lại bot..."), thread_id, thread_type)
            os.execv(sys.executable, [sys.executable] + sys.argv)

        # Lệnh war
        
        elif message.startswith(f"{self.prefix}1c"):
            if message.strip() == f"{self.prefix}1c off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                if self.auto_chatting:
                    self.sendMessage(Message(text=".."), thread_id, thread_type)
                else:
                    filename = "1c.txt" 
                    self.auto_chatting = True
                    self.sendTxt(filename, thread_id, thread_type)

        elif message.startswith(f"{self.prefix}war"):
            if message.strip() == f"{self.prefix}war off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                if self.auto_chatting:
                    self.sendMessage(Message(text=".."), thread_id, thread_type)
                else:
                    filename = "nhay.txt" # Tự thêm ngôn khác =))
                    self.auto_chatting = True
                    self.sendTxt(filename, thread_id, thread_type)

        elif message.startswith(f"{self.prefix}chui"):
            if message.strip() == f"{self.prefix}chui off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                if self.auto_chatting:
                    self.sendMessage(Message(text=".."), thread_id, thread_type)
                else:
                    if not message_object.mentions:
                        self.sendMessage(Message(text="Tag người cần chửi"), thread_id, thread_type)
                        return

                    filename = "nhay.txt"
                    self.auto_chatting = True

                    def send_tagged():
                        try:
                            with open(filename, "r", encoding="utf-8") as f:
                                lines = [line.strip() for line in f if line.strip()]
                            if not lines:
                                self.sendMessage(Message(text="File không có gì"), thread_id, thread_type)
                                self.auto_chatting = False
                                return
                            tagged_uid = message_object.mentions[0]['uid']
                            index = 0
                            while self.auto_chatting:
                                traloi = lines[index] + " @member"
                                offset = len(lines[index]) + 1
                                mention = Mention(tagged_uid, offset=offset, length=8)
                                # print(mention)
                                self.send(
                                    Message(text=traloi, mention=mention),
                                    thread_id,
                                    thread_type
                                )
                                index = (index + 1) % len(lines)
                                for _ in range(10):
                                    if not self.auto_chatting:
                                        break
                                    time.sleep(0.1)
                        except FileNotFoundError:
                            self.sendMessage(Message(text=f"Không tìm thấy file {filename}"), thread_id, thread_type)
                            self.auto_chatting = False
                        except Exception as e:
                            self.sendMessage(Message(text=f"Lỗi: {str(e)}"), thread_id, thread_type)
                            self.auto_chatting = False

                    threading.Thread(target=send_tagged).start()



        elif message.startswith(f"{self.prefix}so"):
            if message.strip() == f"{self.prefix}so off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                if self.auto_chatting:
                    self.sendMessage(Message(text=".."), thread_id, thread_type)
                else:
                    filename = "so.txt" 
                    self.auto_chatting = True
                    self.sendTxt(filename, thread_id, thread_type)

        elif message.startswith(f"{self.prefix}nhay"):
            if message.strip() == f"{self.prefix}nhay off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                if self.auto_chatting:
                    self.sendMessage(Message(text=".."), thread_id, thread_type)
                else:
                    filename = "nhay.txt" 
                    self.auto_chatting = True
                    self.sendTxt(filename, thread_id, thread_type)
        
        elif message.startswith(f"{self.prefix}copy"):
            if message.strip() == f"{self.prefix}copy off":
                self.copy_mode = False
                self.copy_target.clear()
                self.sendMessage(Message(text="Copy mode OFF!"), thread_id, thread_type)
            elif message_object.mentions:
                self.copy_target = set(m['uid'] for m in message_object.mentions)
                self.copy_mode = True
                self.sendMessage(Message(text="Copy mode ON!"), thread_id, thread_type)
            else:
                self.sendMessage(Message(text="Tag người cần copy!"), thread_id, thread_type)

        elif message.startswith(f"{self.prefix}treo"):
            if message.strip() == f"{self.prefix}treo off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                def send_all_repeat():
                    try:
                        with open("ngontreo.txt", "r", encoding="utf-8") as f:
                            content = f.read().strip()
                        if not content:
                            self.sendMessage(Message(text="File khong co gi"), thread_id, thread_type)
                            return
                        self.auto_chatting = True
                        while self.auto_chatting:
                            self.sendMessage(Message(text=content), thread_id, thread_type)
                            time.sleep(5) 
                    except Exception as e:
                        self.sendMessage(Message(text=f"Lỗi: {e}"), thread_id, thread_type)
                        self.auto_chatting = False
                threading.Thread(target=send_all_repeat).start()

        elif message.startswith(f"{self.prefix}xbdz"):
            if message.strip() == f"{self.prefix}xbdz off":
                self.auto_chatting = False
                self.sendMessage(Message(text="Stop!"), thread_id, thread_type)
            else:
                def send_treotagall():
                    try:
                        with open("ngontreo.txt", "r", encoding="utf-8") as f:
                            content = f.read().strip()
                        if not content:
                            self.sendMessage(Message(text="File khong co gi"), thread_id, thread_type)
                            return
                        self.auto_chatting = True
                        group_info = self.fetchGroupInfo(thread_id).gridInfoMap[thread_id]
                        thanhvien = group_info.get('memVerList', [])
                        mention = [Mention(userId.split('_')[0], length=3000, offset=0, auto_format=False) for userId in thanhvien]
                        wjxz_mention = MultiMention(mention)
                        while self.auto_chatting:
                            self.send(Message(text=content, mention=wjxz_mention), thread_id, thread_type)
                            time.sleep(1)
                    except Exception as e:
                        self.sendMessage(Message(text=f"Lỗi: {e}"), thread_id, thread_type)
                        self.auto_chatting = False
                threading.Thread(target=send_treotagall).start()



        elif message.startswith(f"{self.prefix}tagall"):
            if author_id not in self.idadmin:
                noquyen = "Bạn không có quyền để thực hiện điều này!"
                style_error = MultiMsgStyle([
                    MessageStyle(offset=0, length=len(noquyen.encode()), style="font", size="13", auto_format=False),
                    MessageStyle(offset=0, length=len(noquyen.encode()), style="color", color="#cdd6f4", auto_format=False)
                ])
                self.replyMessage(Message(text=noquyen, style=style_error), message_object, thread_id, thread_type)
                return
                content = message.strip().split(' ', 1)
                if len(content) < 2:
                    self.replyMessage(Message(text="Vui lòng nhập nội dung bé ơi"), message_object, thread_id, thread_type)
                    return
                try:
                    wjx = content[1]
                    group_info = self.fetchGroupInfo(thread_id).gridInfoMap[thread_id]
                    thanhvien = group_info.get('memVerList', [])
                    mention = [Mention(userId.split('_')[0], length=3000, offset=0, auto_format=False) for userId in thanhvien]
                    wjxz_mention = MultiMention(mention)
                    self.send(Message(text=wjx, mention=wjxz_mention), thread_id, thread_type)
                except Exception as e:
                    print(f"Error: {e}")


bot = WxBotWar("<API_KEY>", "<SECRET_KEY>", imei=imei, session_cookies=cookies)
bot.listen()
