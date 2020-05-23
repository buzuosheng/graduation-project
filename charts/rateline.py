# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
import pyecharts.options as opts
from pyecharts.charts import Line
import pymysql
from numpy import arange

#连接数据库
conn=pymysql.connect(
    host='localhost',
    user='root',
    passwd='w123456',
    port=3306,
    db='test',
    charset='utf8'
)

#得到可以执行SQL语句的光标对象
cur = conn.cursor()
select_sql = "select rate from tv_tb"
cur.execute(select_sql)
ret = cur.fetchall()
#print(ret)

xli = []
yli = [0]*100

for i in arange(1, 101):
    xli.append(str(float(i)/10))
for j in ret:
    yli[int(float(j[0])*10)] += 1

#print(xli)
#print(yli)

l = (
    Line()
    .add_xaxis(xli)            #x轴坐标点必须是string类型
    .add_yaxis("电视剧部数", yli, is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="电视剧评分分布图"))
)

# 输出保存为图片
make_snapshot(snapshot, l.render("actor.html"), "C:\\Users\\1\\Desktop\\actor.png")
# 保存路径可以自定义，输入图片文件的速度较慢 ，可以先输出网页，测试成功后，再转成图片
print("已生成图片")

cur.close() # 关闭游标
conn.close() # 关闭连接
