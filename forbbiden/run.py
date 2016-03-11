

class Crawler(threading.Thread):

    def __init__(self, cid=0, consumer_key="bkQmaTpWLRd0y0Zd3Yr5ZO98U", consumer_secret="LBVRpn8tyjYrgWbBPwAYpd3XvA0jyE0tqnXV1CMv5RbTWnba4r", access_token="", access_token_secret=""):
        threading.Thread.__init__(self) 
        print "Crawler#%02d - creating" % (cid)
        self.crawlerlog = open("crawler_%02d.log"%cid, "a")
        self.cid = cid
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth_handler=self.auth, wait_on_rate_limit=True)
        self.isEnd = False
        self.logMsg("Initial tweepy.API")
        self.logMsg("Access token : "+self.access_token)
        self.logMsg("Access token secret : "+self.access_token_secret)

    def logMsg(self, st):
        self.crawlerlog.write(time.asctime( time.localtime(time.time()) ) + " " + st + "\n")
        self.crawlerlog.flush()

    def setDBQueue(self, queue):
        self.db_queue = queue

    def setUserQueue(self, queue):
        self.user_queue = queue

    def run(self):
        self.logMsg("Start operation")
        while True:
            key = 0
            if self.isEnd:
                break
            if self.user_queue.empty():
                time.sleep(1)
                continue
            try:
                uid = self.user_queue.get()
                key = uid
                user_detail = self.api.get_user(user_id=uid)
                self.logMsg("Get user detail : %d"%(uid))
                user_obj = {}
                user_obj['uid'] = uid
                user_obj['ujson'] = str(user_detail._json)
                following = self.api.friends_ids(user_id=uid)
                self.logMsg("Get user following : %d"%(uid))
                user_obj['following'] = str(following)
                rand = following[::] 
                if len(rand) > 20:
                    rand = random.sample(rand, 20)
                user_obj['random'] = str(rand)
                #user_obj['following_int'] = following
                self.db_queue.put(str(user_obj))
                self.logMsg("Push user_obj to db_queue : %d"%(uid))
            except tweepy.TweepError as e:
                print "Crawler#%02d : TweepError %d" % (self.cid, key) 
                print e
                self.logMsg("Tweepy Error %d : %s" % (key,str(e)))
                pass
            except:
                print "Crawler#%02d : Error" % (self.cid) 
                traceback.print_exc()
                self.logMsg("Error")
                break

    def rateLimit(self):
        rate = self.api.rate_limit_status()
        print json.dumps(rate, sort_keys=True, indent=4, separators=(',',':'))
        
    def end(self):
        self.isEnd = True
        print "Crawler#%02d - closing" % (self.cid)
        self.logMsg("Close crawler#%02d" % (self.cid))

class DBManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print "DBManager - creating"
        self.conn = sqlite3.connect("twdata.db",check_same_thread=False)
        self.dblog = open("twdata.db.log","a")
        self.logMsg("Open database")
        self.isEnd = False

    def logMsg(self, st):
        self.dblog.write(time.asctime( time.localtime(time.time()) ) + " " + st + "\n")
        self.dblog.flush()

    def run(self):
        self.logMsg("Start operation")
        while True:
            key = 0
            try:
                if self.isEnd :
                    break
                if self.db_queue.empty():
                    time.sleep(1)
                    continue
                user_obj = ast.literal_eval(self.db_queue.get())
                key = user_obj['uid']
                self.conn.execute("INSERT INTO TwUser (uid, ujson, following) VALUES (?,?,?)", (user_obj['uid'], user_obj['ujson'], user_obj['following']))
                self.conn.commit()
                for friend in ast.literal_eval(user_obj['random']):
                    fr_cursor = self.conn.execute(self.strCheckInDatabase(friend))
                    if fr_cursor.fetchone() == None:
                        self.user_queue.put(friend)
                        self.logMsg("Push Data to user_queue : %d" % (friend))
            except sqlite3.IntegrityError:
                print "DBmanager - Key not unique " + str(key)
                self.logMsg("DBManager : Key not unique " + str(key))
                pass
            except:
                print "DBManager : Error"
                traceback.print_exc()
                self.logMsg("DBManager : Error")
                exit()

    def setDBQueue(self, queue):
        self.db_queue = queue

    def setUserQueue(self, queue):
        self.user_queue = queue

    def strCheckInDatabase(self, uid):
        return "SELECT * FROM TwUser WHERE uid = %d" % (uid)

    def strInsert(self, user_obj):
        return "INSERT INTO TwUser (uid, ujson, following) VALUES (%d, '%s', '%s')" % (user_obj['uid'], user_obj['ujson'], user_obj['following'])

    def end(self):
        print "DBManager - closing"
        self.conn.close()
        self.logMsg("Close database")
        self.isEnd = True

if __name__ == "__main__":
    print "=================================="
    print "AchirA Twitter Crawler Version 0.1"
    print "=================================="
    user_queue = Queue.Queue() 
    #user_queue.put(210860010)
    db_queue = Queue.Queue()
    db_obj = None
    db_conn = []
    crawler_obj = [] 
    while True:
        try:
            command = raw_input(">>> ").strip().split()
            if len(command) == 0:
                continue
            elif command[0] == "exit":
                for obj in crawler_obj:
                    obj.end()
                db_obj.end()
                usq = open("user_queue.list", "w")
                usq.write(str(list(user_queue.queue)))
                usq.close()
                dbq = open("db_queue.list", "w")
                dbq.write(str(list(db_queue.queue)))
                dbq.close()
                break
            elif command[0] == "debug":
                dm = DBManager()
                print dm.isEnd
            elif command[0] == "create":
                db_obj = DBManager()
                db_obj.setDBQueue(db_queue)
                db_obj.setUserQueue(user_queue)
                for i in xrange(int(command[1])):
                    config = open("token%02d.cfg"%(i),"r")
                    key = config.readline().split() 
                    obj = Crawler(access_token=key[0],access_token_secret=key[1],cid=i)
                    obj.setDBQueue(db_queue)
                    obj.setUserQueue(user_queue)
                    crawler_obj.append(obj)
                    config.close()
                usq = open("user_queue.list", "r")
                line = ast.literal_eval(usq.readline())
                for i in line:
                    user_queue.put(i)
                usq.close()
                dbq = open("db_queue.list", "r")
                line = ast.literal_eval(dbq.readline())
                for i in line:
                    db_queue.put(i)
                dbq.close()
            elif command[0] == "start":
                db_obj.start()
                for ob in crawler_obj:
                    ob.start()
            elif command[0] == "status":
                print "DBManager : ", db_obj.isAlive()
                print "Crawler :", map(lambda x:x.isAlive(), crawler_obj)
            elif command[0] == "show":
                if len(command) == 1:
                    print "Show nothing"
                elif command[1] == "db_queue":
                    print list(db_queue.queue)
                elif command[1] == "user_queue":
                    print list(user_queue.queue)
                else :
                    print "Show nothing"
            elif command[0] == "reset":
                n = int(command[1])
                config = open("token%02d.cfg"%(n),"r")
                key = config.readline().split() 
                obj = Crawler(access_token=key[0],access_token_secret=key[1],cid=n)
                obj.setDBQueue(db_queue)
                obj.setUserQueue(user_queue)
                crawler_obj[n] = obj
                config.close()
            elif command[0] == "qsize":
                print db_queue.qsize(), user_queue.qsize()
            elif command[0] == "limit":
                n = int(command[1])
                print crawler_obj[n].rateLimit()
            else:
                print "Command not found"
                
        except KeyboardInterrupt:
            print "KeyboardInterrupt - Exit"
            usq = open("user_queue.list", "w")
            usq.write(str(list(user_queue.queue)))
            usq.close()
            dbq = open("db_queue.list", "w")
            dbq.write(str(list(db_queue.queue)))
            dbq.close()
            db_obj.end()
            for ob in crawler_obj:
                ob.end()
            break
        except:
            print "Caught Exception - Exit"
            traceback.print_exc()
            usq = open("user_queue.list", "w")
            usq.write(str(list(user_queue.queue)))
            usq.close()
            dbq = open("db_queue.list", "w")
            dbq.write(str(list(db_queue.queue)))
            dbq.close()
            pass
            #exit()
