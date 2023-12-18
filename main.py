import json
import pickle
import os
import re
import copy
import csv
import random
from collections import OrderedDict
from instagrapi import Client
from matplotlib import pyplot as plt
from collections import Counter
import numpy as np
case=2;
tuple_comments=[];
user_comments=[[] for x in range(15)];
filter_user_comments=[[] for x in range(15)];
comment=[];
comments=[];
likes=[];
f = open('APIFY-comments-likes-links.json')
a=json.load(f);
for i in range (15):
 b=max(range(len(a)), key=lambda index: a[index]['commentsCount'])
 comment.append([b,a[b]['commentsCount']])
 a[b]['commentsCount']=0;
f = open('APIFY-comments-likes-links.json')
a=json.load(f);
for i in range (15):
 b=max(range(len(a)), key=lambda index: a[index]['likesCount'])
 likes.append([b,a[b]['likesCount']])
 a[b]['likesCount']=0;
f = open('APIFY-comments-likes-links.json')
a=json.load(f);

if os.path.isfile('./objs.pkl'):
 with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
  [tuple_comments] = pickle.load(f)
 for i in range(0,len(tuple_comments)):
  for j in range(0,len(tuple_comments[i])):
   tuple_comments[i][j]=tuple_comments[i][j].dict();

else:
 cl = Client()
 cl.login('#######', '######')
 for i in range(0,1): #range(len(tuple_comments),len(comment)):
  media_id = cl.media_id(cl.media_pk_from_url(a[comment[i][0]]['url']))
  comments = cl.media_comments(media_id,0)
  tuple_comments.append(comments);
  with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
   pickle.dump([tuple_comments], f)
def replace_int(number):
 if number.is_integer():
    return int(number)
 else: return number

for i in range(len(tuple_comments)):
 for j in range(len(tuple_comments[i])):
  user_comments[i].append((tuple_comments[i][j]['user']['username'],list(map(replace_int,list(map(float,re.findall(r"[-+]?(?:\d*\.*\d+)",tuple_comments[i][j]['text'])))))))

for post in user_comments:
 for comment_post in post:
  for number in list(comment_post[1]):
   if number<34 or number>48:
    comment_post[1].remove(number)


for post in user_comments:
  for comment_post in list(post):
    if len(comment_post[1])>1:
     print(comment_post)
    elif not comment_post[1]:
     post.remove(comment_post)
# group by user:comments, filter on user instead of multiple
i=0;
for post in user_comments:
 for comment_post in list(post):
  if comment_post[0] not in [post[0] for post in filter_user_comments[i]]:
   filter_user_comments[i].append(comment_post);
  else:
   filter_user_comments[i][-1][1].extend(comment_post[1])
 i+=1;




method=2;#define which method to use




 #method 1: random number in sizes// keep only one random ex: user comments of user g.a={43,43,43,43,43,44} take random
filter_user_comments_1=copy.deepcopy(filter_user_comments);
filter_user_comments_2=copy.deepcopy(filter_user_comments);
if method==1:
 for post in filter_user_comments_1:
  for comment_post in list(post):
    tmp=random.choice(comment_post[1]);
    comment_post[1].clear();
    comment_post[1].append(tmp)
 # Creating dataset
 #test1=[x[0] for x in [post[1] for post in filter_user_comments_1[0]]];
 aa = [Counter([x[0] for x in [post[1] for post in filter_user_comments_1[i]]]) for i in range(len(filter_user_comments_1))]
 aa=list(map(dict,aa));
 for i in range(len(comment)):
  aa[i]=OrderedDict(sorted(aa[i].items(), key=lambda t: t[0]))
 for i in range(len(comment)):
  aa[i].update({'caption':a[comment[i][0]]['caption'],'url':a[comment[i][0]]['url']})

# labels, counts = np.unique(a, return_counts=True)
# plt.subplot(2, 1, 1)
# plt.title("method1")
# plt.bar(labels, counts, align='center')
# plt.gca().set_xticks(labels)
# plt.gca().set_yticks(counts)


 #method 2: remove comments of user multiple comments// ex: user comments of user g.a={43,43,43,43,43,44} remove all comments of g.a, g.b={43,43,43,43,43,43} keep 43
else:
 for post in filter_user_comments_2:
  for comment_post in list(post):
    if len(list(set(comment_post[1])))>1:
     post.remove(comment_post);
 #test2=[x[0] for x in [[random.choice(post[1])] for post in filter_user_comments_2[0]]]
 # Creating dataset
 aa = [Counter([x[0] for x in [[random.choice(post[1])] for post in filter_user_comments_2[i]]]) for i in range(len(filter_user_comments_2))]
 aa=list(map(dict,aa))
 for i in range(len(comment)):
  aa[i]=OrderedDict(sorted(aa[i].items(), key=lambda t: t[0]))
 for i in range(len(comment)):
  aa[i].update({'caption':a[comment[i][0]]['caption'],'url':a[comment[i][0]]['url']})

# csv part
for i in range(len(comment)):
 with open('mycsvfile'+str(i)+'.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
  w = csv.DictWriter(f, aa[i].keys())
  w.writeheader()
  w.writerow(aa[i])
# except IOError:
#     print("I/O error")




    # Creating histogram
    #fig, ax = plt.subplots(figsize=(10, 7))
# labels, counts = np.unique(b, return_counts=True)
# plt.subplot(2, 1, 2)
# plt.title("method2:remove when different")
# plt.bar(labels, counts, align='center')
# plt.gca().set_xticks(labels)
# plt.gca().set_yticks(counts)
# plt.show()
print("")
