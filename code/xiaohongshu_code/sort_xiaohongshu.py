# 定义字典
import matplotlib.pyplot as plt
import json
with open('/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_classes.json','r',encoding='utf-8')as file:
    d = json.loads(file.read())

# 对字典按照值进行排序
sorted_values = sorted(d.values(), reverse=True)

# 计算前100个值的和和所有值的和
list_step = []
list_percentage = []
for i in range(1000,1000000,10000):
    top100_sum = sum(sorted_values[:i])
    total_sum = sum(sorted_values)
    list_step.append(i)
    list_percentage.append((top100_sum/total_sum)*100)


plt.bar(range(len(list_step)), list_step)
# 设置 x 轴标签和刻度
plt.xticks(range(len(list_step)), list_step, rotation=90)
plt.xlabel('step')

# 设置 y 轴标签和刻度
plt.ylabel('percentage')
plt.yticks(range(int(max(list_percentage)+1)))

# 显示图形
plt.show()

