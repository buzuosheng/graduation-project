import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt

conn=pymysql.connect(
    host='localhost',
    user='root',
    passwd='w123456',
    port=3306,
    db='tv',
    charset='utf8'
)

cur = conn.cursor()
select_sql = "select tv_type from tv_tb"
cur.execute(select_sql)
ret = cur.fetchall()
# print(ret)

data = []
for i in ret:
  data.append(i[0].replace('/', ' '))
text = ' '.join(data)
# print(text)

wc = WordCloud(font_path='simsun.ttc', collocations=False, width=800, height=600, mode='RGBA', background_color=None).generate(text)

# 显示词云
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()

# 保存到文件
wc.to_file('C:\\Users\\1\\Desktop\\wcType.png')  # 生成图像是透明的
print("已生成词云图")