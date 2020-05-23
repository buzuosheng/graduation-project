from pyecharts.charts import Pie#饼图所导入的包
from pyecharts import options as opts#全局设置所导入的包
import pymysql
from collections import Counter

conn=pymysql.connect(
    host='localhost',
    user='root',
    passwd='w123456',
    port=3306,
    db='tv',
    charset='utf8'
)

cur = conn.cursor()
select_sql = "select c_or_r from tv_tb"
cur.execute(select_sql)
ret = cur.fetchall()
# print(ret)

data = []
for i in ret:
  data.append(i[0].split('/')[0])

newdata = []
num_count = Counter(data)
for item in num_count:
  newdata.append([item, num_count[item]])

def Pie1():
  pie = (
  Pie()
  .add("", newdata)
  .set_global_opts(title_opts=opts.TitleOpts(title="Pie-国家或地区"),legend_opts=opts.LegendOpts(pos_left=160))
  .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")))
  return pie

Pie1().render('C:\\Users\\1\\Desktop\\c_or_rPie.html')