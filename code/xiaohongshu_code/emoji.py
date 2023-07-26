text_with_emoji = '宝宝辅食20种菜泥做法汇总📒干货🔥\n宝宝初期菜泥辅食做法汇总📒建议收藏，基本上都是我家娃吃过的，做法我之前也有发过，这次整理了一下～\n1.西兰花泥🥦\n做法：约100~150g西兰花，用水浸泡10分钟，切小块放入沸水焯熟，放入料理机打泥即可。\n2.豌豆泥\n做法：约一小把豌豆，洗净上锅蒸15分钟，放入料理机打泥，豌豆有皮可以进行过筛一遍更加细腻。\n3.土豆泥🥔\n做法'
import re

emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]", flags=re.UNICODE)

# text_with_emoji = "This is a text with some 😄😂🙏 emoji 😊👍🏼👎🏼."
emojis = emoji_pattern.findall(text_with_emoji)
print(emojis)


