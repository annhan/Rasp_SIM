#!/usr/bin/env python

from __future__ import print_function
from socket import AF_INET, SOCK_DGRAM
import sys;
import socket;
import select;
import thread;
import pickle;
import struct;
import time;
import os
import sys, threading, logging
import subprocess
import os
import SimpleHTTPServer
import SocketServer
import hc2

dulieu=''
SIZEOF_UINT32 = 4
PORT = '/dev/ttyAMA0'
BAUDRATE = 9600
PIN = None
sdtdanhba={'1':'NULL','2':'NULL','3':'NULL','4':'NULL'}
diachihc2={'ip':'192.168.1.4','user':'admin','password':'admin'}
diachihc2={'ip':'192.168.1.40','gataway':'192.68.1.1','netmask':'255.255.255.0'}
trangthaitk=0
t=None
from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException, CommandError
waitForCallback = True
trangthaicuocgoi=0
sottgoi=0
class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
        self.PORTNO=10001;
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        self.s.bind(("0.0.0.0",self.PORTNO));
        self.CONNECTION_LIST=[];
        self.RECV_BUFFER=4096;
    def run(self):
        self.s.listen(5)
        while(1):
            c,addr = self.s.accept()
            print(addr)
            print(c)
            try:
                data=bytes.decode(c.recv(1024))
                if data:
                    thread.start_new_thread(recv,(data,));
            except:
                dulieu=""
            c.send(b'Ket noi thanh cong !')
            c.close()
def recv(data):
    dulieu=data
    global trangthaitk
    if "IPHC2:" in dulieu:
        diachihc2['ip']=dulieu[dulieu.find("IPHC2:")+6:]
        f = open('hc2.txt','w+')
        f.write("ip:{}*\r\n".format(diachihc2['ip']))
        f.write("user:{}.\r\n".format(diachihc2['user']))
        f.write("pass:{}.\r\n".format(diachihc2['password']))
        f.close()
    if "userHC2:" in dulieu:
        diachihc2['user']=dulieu[dulieu.find("userHC2:")+8:]
        f = open('hc2.txt','w+')
        f.write("ip:{}*\r\n".format(diachihc2['ip']))
        f.write("user:{}.\r\n".format(diachihc2['user']))
        f.write("pass:{}.\r\n".format(diachihc2['password']))
        f.close()
    if "passHC2:" in dulieu:
        diachihc2['password']=dulieu[dulieu.find("passHC2:")+8:]
        f = open('hc2.txt','w+')
        f.write("ip:{}*\r\n".format(diachihc2['ip']))
        f.write("user:{}.\r\n".format(diachihc2['user']))
        f.write("pass:{}.\r\n".format(diachihc2['password']))
        f.close()
    if "hc2kiemtra" in dulieu:
        c.send("dabat")
    if "TATAN" in dulieu:
        guitinnhan('HC2 OFF Alarm')
    if "BATAN" in dulieu:
        guitinnhan('HC2 On Alarm')
    if "TK" in dulieu:
        trangthaitk=0
        vitri=dulieu.find('"')
        vitricuoi=dulieu.find('"',vitri+1)
        noidung=dulieu[vitri+1:vitricuoi].encode("utf-8")
        KTTK(noidung)
    if "CALL" in dulieu:
        global sottgoi
        sottgoi=1
        KTTK(sdtdanhba['1'])
    if "SMS" in dulieu:
        vitri=dulieu.find('"')
        vitricuoi=dulieu.find('"',vitri+1)
        noidungsms=dulieu[vitri+1:vitricuoi].encode("utf-8")
        guitinnhan(noidungsms)
    if "sdt1" in dulieu:
        vitri=dulieu.find('sdt1:')
        sodt=dulieu[vitri+6:dulieu.find('.',vitri+6)]
        sdtdanhba['1']=sodt.encode("utf-8")
	print(sdtdanhba['1'])
	if len(sdtdanhba['1'])>9:
	    ghidanhba(1,sdtdanhba['1'])
	elif len(sdtdanhba['1'])<9:
	    ghidanhba(1,'0')
	    sdtdanhba['1']='NULL'
    if "sdt2" in dulieu:
        vitri=dulieu.find('sdt2:')
        sodt=dulieu[vitri+6:dulieu.find('.',vitri+6)]
        sdtdanhba['2']=sodt.encode("utf-8")
	print(sdtdanhba['2'])
	if len(sdtdanhba['2'])>9:
	    ghidanhba(2,sdtdanhba['2'])
	elif len(sdtdanhba['2'])<9:
	    ghidanhba(2,'0')
	    sdtdanhba['2']='NULL'
    if "sdt3" in dulieu:
        vitri=dulieu.find('sdt3:')
        sodt=dulieu[vitri+6:dulieu.find('.',vitri+6)]
        sdtdanhba['3']=sodt.encode("utf-8")
	print(sdtdanhba['3'])
	if len(sdtdanhba['3'])>9:
	    ghidanhba(3,sdtdanhba['3'])
	elif len(sdtdanhba['3'])<9:
	    ghidanhba(3,'0')
	    sdtdanhba['3']='NULL'
    if "sdt4" in dulieu:
        vitri = dulieu.find('sdt4:')
        sodt = dulieu[vitri+6:dulieu.find('.',vitri+6)]
        sdtdanhba['4'] = sodt.encode("utf-8")
	print(sdtdanhba['4'])
	if len(sdtdanhba['4'])>9:
	    ghidanhba(4,sdtdanhba['4'])
	elif len(sdtdanhba['4'])<9:
	    ghidanhba(4,'0')
	    sdtdanhba['4']='NULL'
def handleIncomingCall(call):
    print('co cuoc goi {}'.format(call.number))
    if call.ringCount == 1:
        print('Incoming call from:', call.callerName)
        print('Incoming call from:', call.ringCount)
    elif call.ringCount >= 2:
        if (call.number==sdtdanhba['1']) or (call.number==sdtdanhba['2']) or (call.number==sdtdanhba['3']) or (call.number==sdtdanhba['4']):
            print("co cuoc goi den")
            modem.write('ATA')
            anninh=hc2.getvariable('AN_Kichhoat')
            anninh=anninh.json()
            print(anninh['value'])
            if int(anninh['value'])==1:
                print("1")
                hc2.setvariable('AN_Kichhoat','0')
                guitinnhan('SDT: {} Turn Off Alarm'.format(call.number))
            elif int(anninh['value'])==0:
                print("0")
                hc2.setvariable('AN_Kichhoat','1')
                guitinnhan('SDT: {} Turn On Alarm'.format(call.number))
        else:
            modem.write('ATH')
            call.hangup()
def kttaikhoan():
    global trangthaitk,t
    trangthaitk=1
    KTTK('*101#')
    t = threading.Timer(43200.0, kttaikhoan)
    t.start()
def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    if 'IP' in sms.text:
	trungiang=sms.text
	vitri=sms.text.find('IP:')
	vitrigiua=sms.text.find(',',vitri+6)
        f = open('/etc/network/interfaces','w+')
	f.write("auto lo\r\n")
	f.write("iface lo inet loopback\r\n")
	f.write("iface eth0 inet static\r\n")
        f.write("address {}\r\n".format(sms.text[vitri+3:vitrigiua]))
        f.write("gateway {}\r\n".format(sms.text[vitrigiua+1:]))
        f.write("netmask {}\r\n".format("255.255.255.0"))
        f.close()
	guitinnhan1(sms.number,'Set IP Xong. Khoi Dong lai Board'.format(sms.number))
    if (sms.number==sdtdanhba['1']) or (sms.number==sdtdanhba['2']) or (sms.number==sdtdanhba['3']) or (sms.number==sdtdanhba['4']):
        if 'ON' in sms.text.upper() and len(sms.text)<5:
            hc2.setvariable('AN_Kichhoat','1')
            guitinnhan('SDT: {} Turn On Alarm'.format(sms.number))
        elif 'OFF' in sms.text.upper() and len(sms.text)<5:
            hc2.setvariable('AN_Kichhoat','0')
            guitinnhan('SDT: {} Turn Off Alarm'.format(sms.number))
        elif 'OK' in sms.text.upper() and len(sms.text)<5:
            hc2.setvariable('AN_Kichhoat','0')
            guitinnhan('SDT: {} Turn Off Alarm'.format(sms.number))
        elif 'STK' in sms.text.upper():
            sms.text=sms.text.upper()
            MATHE='*100*{}#'.format(sms.text[sms.text.find("STK")+3:])
            KTTK(MATHE)
        elif 'KTTK' in sms.text.upper():
            sms.text=sms.text.upper()
            KTTK(sms.text[sms.text.find("KTTK")+4:])
        else:
            guitinnhan('SDT: {} Sai cu phap'.format(sms.number))
    else:
        if 'ON' in sms.text and len(sms.text)<5:
            guitinnhan('ALARM  SDT: {}  Turn On Alarm Fail'.format(sms.number))
        elif 'OFF' in sms.text and len(sms.text)<5:
            guitinnhan('ALARM  SDT: {} Turn Off Alarm Fail'.format(sms.number))
        elif 'STK' in sms.text.upper():
            sms.text=sms.text.upper()
            MATHE='*100*{}#'.format(sms.text[sms.text.find("STK")+3:])
            KTTK(MATHE)
        elif 'KTTK' in sms.text.upper():
            sms.text=sms.text.upper()
            KTTK(sms.text[sms.text.find("KTTK")+4:])
def danhba(s):
    print(s['thutu'])
    if s['thutu']=='1':
        sdtdanhba['1']=s['sodienthoai']
    if s['thutu']=='2':
        sdtdanhba['2']=s['sodienthoai']
    if s['thutu']=='3':
        sdtdanhba['3']=s['sodienthoai']
    if s['thutu']=='4':
        sdtdanhba['4']=s['sodienthoai']
	if len(sdtdanhba['4'])<9:
	    sdtdanhba['4']='NULL'
def tongdai(noidungtongdai):
    global trangthaitk
    if trangthaitk==0:
        guitinnhan(noidungtongdai)
    elif 'TK chinh' in noidungtongdai:
        vitri=noidungtongdai.find('TK chinh=')
        vitricuoi=noidungtongdai.find(' ',vitri+5)
        sotien=int(noidungtongdai[vitri+9:vitricuoi])
        if sotien>10000:
            print("nho hon 10.000d")
        if sotien<10000:
            print("lon hon")
            guitinnhan("Chu y: Tai Khoan Quy Khach Con Duoi 10.000d.")
        print(sotien)
        trangthaitk=0
def cuocgoi(noidung):
    print(noidung)
    global sottgoi
    if sottgoi<5:
        if noidung=='NO CARRIER':
            print("Da tra loi")
        elif noidung=='NO ANSWER' or noidung=='BUSY':
            if sottgoi==4:
                print('hetso dt')
            else:
                sottgoi+=1
                while sdtdanhba[str(sottgoi)]=='NULL' and sottgoi<4:
                    sottgoi+=1
                    print('khong co so {}'.format(sottgoi))
                if sdtdanhba[str(sottgoi)]!='NULL':
                    KTTK(sdtdanhba[str(sottgoi)])
def ghidanhba(stt,sdt):
    print(sdt)
    modem.write('AT+CPBW={0},"{1}",129,""'.format(stt,sdt.encode("utf-8")))
def KTTK(sotk):
    modem.write('ATD{};'.format(sotk.encode("utf-8")))
def guitinnhan1(sdt,noidung):
    modem.sendSms(sdt,noidung.encode("utf-8"))
def guitinnhan(noidung):
    if sdtdanhba['1']!='NULL':
        modem.sendSms(sdtdanhba['1'],noidung.encode("utf-8"))
        time.sleep(2)
    if sdtdanhba['2']!='NULL':
        modem.sendSms(sdtdanhba['2'],noidung.encode("utf-8"))
        time.sleep(2)
    if sdtdanhba['3']!='NULL':
        modem.sendSms(sdtdanhba['3'],noidung.encode("utf-8"))
        time.sleep(2)
    if sdtdanhba['4']!='NULL':
        modem.sendSms(sdtdanhba['4'],noidung.encode("utf-8"))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
modem = GsmModem(PORT, BAUDRATE,incomingCallCallbackFunc=handleIncomingCall, smsReceivedCallbackFunc=handleSms,danhbacallbackfun=danhba,tongdaicallbackfun=tongdai,statuscallcallbackfun=cuocgoi)
modem.smsTextMode = True
modem.connect(PIN)
server_thread=server();
server_thread.start();
filetxt = open('hc2.txt','r')
noidunghc2=filetxt.read()
try:
    if "ip" in noidunghc2:
        vitri=noidunghc2.find("ip")+3
        diachihc2['ip']=str(noidunghc2[vitri:noidunghc2.find("*",vitri)])
        print(diachihc2['ip'])
except:
    diachihc2['ip']='192.168.1.4'
try:
    if "user" in noidunghc2:
        vitri=noidunghc2.find("user")+5
        diachihc2['user']=str(noidunghc2[vitri:noidunghc2.find(".",vitri)])
        print(diachihc2['user'])
except:
    diachihc2['user']='admin'
try:
    if "pass" in noidunghc2:
        vitri=noidunghc2.find("pass")+5
        diachihc2['password']=str(noidunghc2[vitri:noidunghc2.find(".",vitri)])
        print(diachihc2['password'])
except:
    diachihc2['password']='admin'
hc2=hc2.hc2(diachihc2['user'],diachihc2['password'],diachihc2['ip'])
#hc2.setvariable('an_ninh','1')
if __name__ == "__main__":
    modem.write('AT+CPBR=1')
    modem.write('AT+CPBR=2')
    modem.write('AT+CPBR=3')
    modem.write('AT+CPBR=4')
    modem.waitForNetworkCoverage(30)
    time.sleep(1)
    t = threading.Timer(30.0, kttaikhoan)
    t.start()
    try:
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close();
    sys.exit(app.exec_())

